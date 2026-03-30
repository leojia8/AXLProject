/**
 * game.js -- AI Feud Game Controller
 *
 * Features: timer, sound effects (with mute toggle), strike popup,
 * auto-recovery from stale round IDs, AI tooltip.
 */

// ===========================================================================
// STATE
// ===========================================================================
let currentRoundId = null;
let isLoading = false;
let maxStrikes = 3;
let timerInterval = null;
let timeRemaining = 60;
const ROUND_TIME = 60;
let soundEnabled = true;
let strikePopupTimeout = null;
let currentStrikes = 0;

// ===========================================================================
// SOUND EFFECTS (Web Audio API)
// ===========================================================================

const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function ensureAudio() {
    if (!audioCtx) audioCtx = new AudioCtx();
    return audioCtx;
}

function playCorrectSound() {
    if (!soundEnabled) return;
    try {
        const ctx = ensureAudio();
        [0, 0.12].forEach((delay, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sine';
            osc.frequency.value = i === 0 ? 523.25 : 659.25;
            gain.gain.setValueAtTime(0.3, ctx.currentTime + delay);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 0.3);
            osc.start(ctx.currentTime + delay);
            osc.stop(ctx.currentTime + delay + 0.3);
        });
    } catch (e) {}
}

function playWrongSound() {
    if (!soundEnabled) return;
    try {
        const ctx = ensureAudio();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sawtooth';
        osc.frequency.value = 120;
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.4);
    } catch (e) {}
}

function playWinSound() {
    if (!soundEnabled) return;
    try {
        const ctx = ensureAudio();
        const notes = [523.25, 659.25, 783.99, 1046.5];
        notes.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sine';
            osc.frequency.value = freq;
            const t = ctx.currentTime + i * 0.15;
            gain.gain.setValueAtTime(0.25, t);
            gain.gain.exponentialRampToValueAtTime(0.001, t + 0.4);
            osc.start(t);
            osc.stop(t + 0.4);
        });
    } catch (e) {}
}

function playLoseSound() {
    if (!soundEnabled) return;
    try {
        const ctx = ensureAudio();
        const notes = [392, 349.23, 311.13, 261.63];
        notes.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'triangle';
            osc.frequency.value = freq;
            const t = ctx.currentTime + i * 0.25;
            gain.gain.setValueAtTime(0.25, t);
            gain.gain.exponentialRampToValueAtTime(0.001, t + 0.5);
            osc.start(t);
            osc.stop(t + 0.5);
        });
    } catch (e) {}
}

function playTimerBeep() {
    if (!soundEnabled) return;
    try {
        const ctx = ensureAudio();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.value = 880;
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.1);
    } catch (e) {}
}


// ===========================================================================
// DOM REFERENCES
// ===========================================================================
const $ = (sel) => document.querySelector(sel);
let els = {};

function cacheDom() {
    els = {
        loadingScreen: $('#loading-screen'),
        gameArea: $('#game-area'),
        promptText: $('#prompt-text'),
        answerBoard: $('#answer-board'),
        scoreDisplay: $('#score-display'),
        guessForm: $('#guess-form'),
        guessInput: $('#guess-input'),
        submitBtn: $('#submit-btn'),
        roundOverOverlay: $('#round-over-overlay'),
        overlayTitle: $('#overlay-title'),
        finalBoard: $('#final-board'),
        finalScore: $('#final-score'),
        finalStrikes: $('#final-strikes'),
        playAgainBtn: $('#play-again-btn'),
        timerBar: $('#timer-bar'),
        timerDisplay: $('#timer-display'),
        timerBox: $('.timer-box'),
        strikePopup: $('#strike-popup'),
        strikeXs: $('#strike-xs'),
        strikeGuessText: $('#strike-guess-text'),
        soundToggle: $('#sound-toggle'),
        soundIcon: $('#sound-icon'),
        aiInfoBtn: $('#ai-info-btn'),
        aiTooltipText: $('#ai-tooltip-text'),
    };
}


// ===========================================================================
// INITIALIZATION
// ===========================================================================
document.addEventListener('DOMContentLoaded', () => {
    cacheDom();
    attachEventListeners();
    startNewRound();
});

function attachEventListeners() {
    els.guessForm.addEventListener('submit', handleSubmit);
    els.playAgainBtn.addEventListener('click', handleNewRound);

    // Sound toggle
    els.soundToggle.addEventListener('click', () => {
        soundEnabled = !soundEnabled;
        els.soundIcon.textContent = soundEnabled ? 'SOUND ON' : 'SOUND OFF';
        els.soundToggle.classList.toggle('muted', !soundEnabled);
    });

    // AI tooltip toggle
    els.aiInfoBtn.addEventListener('click', () => {
        els.aiTooltipText.classList.toggle('hidden');
    });

    // Close tooltip on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.ai-tooltip')) {
            els.aiTooltipText.classList.add('hidden');
        }
    });
}


// ===========================================================================
// TIMER
// ===========================================================================

function startTimer() {
    stopTimer();
    timeRemaining = ROUND_TIME;
    updateTimerDisplay();

    timerInterval = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();

        if (timeRemaining <= 10 && timeRemaining > 0) {
            playTimerBeep();
        }

        if (timeRemaining <= 0) {
            stopTimer();
            handleTimeUp();
        }
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function updateTimerDisplay() {
    const pct = Math.max(0, (timeRemaining / ROUND_TIME) * 100);
    els.timerBar.style.width = pct + '%';
    els.timerDisplay.textContent = timeRemaining;

    els.timerBar.classList.remove('warning', 'danger');
    els.timerBox.classList.remove('warning', 'danger');

    if (timeRemaining <= 10) {
        els.timerBar.classList.add('danger');
        els.timerBox.classList.add('danger');
    } else if (timeRemaining <= 20) {
        els.timerBar.classList.add('warning');
        els.timerBox.classList.add('warning');
    }
}

async function handleTimeUp() {
    els.guessInput.disabled = true;
    els.submitBtn.disabled = true;

    playLoseSound();

    const revealData = await revealBoard();
    els.overlayTitle.textContent = "TIME'S UP!";

    if (revealData) {
        els.finalBoard.innerHTML = '';
        revealData.board.forEach(slot => {
            els.finalBoard.appendChild(createSlotElement(slot));
        });
        els.finalScore.textContent = revealData.score;
        els.finalStrikes.textContent = `${revealData.strikes} / ${maxStrikes}`;
    }

    els.roundOverOverlay.classList.remove('hidden');
}


// ===========================================================================
// API CALLS
// ===========================================================================

async function startNewRound() {
    setLoading(true);
    currentStrikes = 0;

    try {
        const res = await fetch('/api/new-round', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prefer_real: true }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        currentRoundId = data.round_id;
        maxStrikes = data.max_strikes;

        renderNewRound(data);
        setLoading(false);
        startTimer();
    } catch (err) {
        console.error('Failed to start round:', err);
        setLoading(false);
        showError('Failed to load round. Please refresh.');
    }
}

async function submitGuess(guess) {
    if (isLoading || !currentRoundId || timeRemaining <= 0) return;
    setInputLoading(true);

    try {
        const res = await fetch('/api/guess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ round_id: currentRoundId, guess }),
        });

        if (res.status === 404 || res.status === 400) {
            // Round expired or already over. Auto-start new round.
            console.warn('Round stale, starting new round...');
            setInputLoading(false);
            startNewRound();
            return;
        }

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `HTTP ${res.status}`);
        }

        const data = await res.json();
        handleGuessResult(data, guess);
    } catch (err) {
        console.error('Guess failed:', err);
        if (err.message === 'Round not found') {
            startNewRound();
            return;
        }
        showError(err.message || 'Failed to submit guess.');
    } finally {
        setInputLoading(false);
        clearInput();
    }
}

async function revealBoard() {
    try {
        const res = await fetch('/api/reveal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ round_id: currentRoundId }),
        });
        if (res.status === 404) return null;
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error('Reveal failed:', err);
        return null;
    }
}


// ===========================================================================
// RENDERING
// ===========================================================================

function renderNewRound(data) {
    els.promptText.textContent = data.prompt;
    renderBoard(data.board);
    renderScore(data.score);
    hideRoundOver();
    hideStrikePopup();
    els.guessInput.disabled = false;
    els.submitBtn.disabled = false;
    els.guessInput.focus();
}

function renderBoard(slots) {
    els.answerBoard.innerHTML = '';
    slots.forEach((slot) => {
        els.answerBoard.appendChild(createSlotElement(slot));
    });
}

function createSlotElement(slot) {
    const div = document.createElement('div');
    div.className = `answer-slot ${slot.revealed ? 'slot-revealed' : 'slot-hidden'}`;
    div.dataset.rank = slot.rank;

    if (slot.revealed) {
        div.innerHTML = `
            <div class="slot-content">${escapeHtml(slot.text).toUpperCase()}</div>
            <div class="slot-score">${slot.score}</div>
        `;
    } else {
        div.innerHTML = `<div class="slot-number">${slot.rank}</div>`;
    }

    return div;
}

function renderScore(score) {
    els.scoreDisplay.textContent = score;
}


// ===========================================================================
// STRIKE POPUP (big red X overlay)
// ===========================================================================

function showStrikePopup(strikes, guess) {
    if (strikePopupTimeout) clearTimeout(strikePopupTimeout);

    // Build X icons -- each in its own separate box
    let xsHtml = '';
    for (let i = 0; i < strikes; i++) {
        xsHtml += '<div class="strike-x-box"><span class="strike-x-icon">X</span></div>';
    }
    els.strikeXs.innerHTML = xsHtml;
    els.strikeGuessText.textContent = guess.toUpperCase();

    els.strikePopup.classList.remove('hidden');

    // Auto-hide after 1.2 seconds (unless round is over)
    strikePopupTimeout = setTimeout(() => {
        hideStrikePopup();
    }, 1200);
}

function hideStrikePopup() {
    els.strikePopup.classList.add('hidden');
    if (strikePopupTimeout) {
        clearTimeout(strikePopupTimeout);
        strikePopupTimeout = null;
    }
}


// ===========================================================================
// GUESS RESULT HANDLING
// ===========================================================================

function handleGuessResult(data, guess) {
    renderBoard(data.board);
    renderScore(data.score);
    currentStrikes = data.strikes;

    if (data.correct) {
        playCorrectSound();
        els.guessInput.classList.add('flash-correct');
        setTimeout(() => els.guessInput.classList.remove('flash-correct'), 500);
    } else {
        playWrongSound();
        els.guessInput.classList.add('flash-incorrect');
        setTimeout(() => els.guessInput.classList.remove('flash-incorrect'), 500);

        // Show big X popup
        showStrikePopup(data.strikes, guess);
    }

    if (data.round_over) {
        stopTimer();
        // Delay to let strike popup show
        setTimeout(() => {
            hideStrikePopup();
            showRoundOver(data);
        }, data.correct ? 300 : 1400);
    }
}


// ===========================================================================
// ROUND OVER
// ===========================================================================

async function showRoundOver(data) {
    els.guessInput.disabled = true;
    els.submitBtn.disabled = true;

    const revealData = await revealBoard();

    const allRevealed = data.board.every(s => s.revealed);
    if (allRevealed) {
        els.overlayTitle.textContent = 'PERFECT ROUND!';
        playWinSound();
    } else if (data.strikes >= maxStrikes) {
        els.overlayTitle.textContent = 'STRUCK OUT!';
        playLoseSound();
    } else {
        els.overlayTitle.textContent = 'ROUND OVER';
        playLoseSound();
    }

    if (revealData) {
        els.finalBoard.innerHTML = '';
        revealData.board.forEach(slot => {
            els.finalBoard.appendChild(createSlotElement(slot));
        });
        els.finalScore.textContent = revealData.score;
        els.finalStrikes.textContent = `${revealData.strikes} / ${maxStrikes}`;
    } else {
        els.finalScore.textContent = data.score;
        els.finalStrikes.textContent = `${data.strikes} / ${maxStrikes}`;
    }

    els.roundOverOverlay.classList.remove('hidden');
}

function hideRoundOver() {
    els.roundOverOverlay.classList.add('hidden');
}


// ===========================================================================
// UI HELPERS
// ===========================================================================

function setLoading(loading) {
    isLoading = loading;
    if (loading) {
        els.loadingScreen.classList.remove('hidden');
        els.gameArea.classList.add('hidden');
    } else {
        els.loadingScreen.classList.add('hidden');
        els.gameArea.classList.remove('hidden');
    }
}

function setInputLoading(loading) {
    els.guessInput.disabled = loading;
    els.submitBtn.disabled = loading;
    els.submitBtn.textContent = loading ? '...' : 'SUBMIT';
}

function clearInput() {
    els.guessInput.value = '';
    els.guessInput.focus();
}

function showError(message) {
    console.error(message);
    const existing = document.querySelector('.error-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        background: #ff4136; color: white; padding: 0.75rem 1.5rem;
        border-radius: 10px; font-size: 0.875rem; z-index: 300;
        animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ===========================================================================
// EVENT HANDLERS
// ===========================================================================

function handleSubmit(e) {
    e.preventDefault();
    const guess = els.guessInput.value.trim();
    if (!guess) return;
    submitGuess(guess);
}

function handleNewRound() {
    startNewRound();
}
