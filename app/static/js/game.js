/**
 * game.js — Client-Side Game Controller
 *
 * Drives all gameplay via fetch() calls to /api/* endpoints.
 * Client renders state from server — never stores answers locally.
 */

// ===========================================================================
// STATE
// ===========================================================================
let currentRoundId = null;
let isLoading = false;
let maxStrikes = 3;

// ===========================================================================
// DOM REFERENCES
// ===========================================================================
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

let els = {};

function cacheDom() {
    els = {
        loadingScreen: $('#loading-screen'),
        gameArea: $('#game-area'),
        promptText: $('#prompt-text'),
        sourceBadge: $('#source-badge'),
        categoryBadge: $('#category-badge'),
        answerBoard: $('#answer-board'),
        scoreDisplay: $('#score-display'),
        strikesDisplay: $('#strikes-display'),
        guessForm: $('#guess-form'),
        guessInput: $('#guess-input'),
        submitBtn: $('#submit-btn'),
        guessList: $('#guess-list'),
        roundOverOverlay: $('#round-over-overlay'),
        overlayTitle: $('#overlay-title'),
        finalBoard: $('#final-board'),
        finalScore: $('#final-score'),
        finalStrikes: $('#final-strikes'),
        commentary: $('#commentary'),
        playAgainBtn: $('#play-again-btn'),
    };
}


// ===========================================================================
// INITIALIZATION
// ===========================================================================
document.addEventListener('DOMContentLoaded', () => {
    cacheDom();
    attachEventListeners();
    startNewRound(window.__INITIAL_CATEGORY__);
});

function attachEventListeners() {
    els.guessForm.addEventListener('submit', handleSubmit);
    els.playAgainBtn.addEventListener('click', handleNewRound);
}


// ===========================================================================
// API CALLS
// ===========================================================================

async function startNewRound(category = null) {
    setLoading(true);
    try {
        const body = { prefer_real: true };
        if (category) body.category = category;

        const res = await fetch('/api/new-round', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        currentRoundId = data.round_id;
        maxStrikes = data.max_strikes;

        renderNewRound(data);
        setLoading(false);
    } catch (err) {
        console.error('Failed to start round:', err);
        setLoading(false);
        showError('Failed to load round. Please refresh.');
    }
}

async function submitGuess(guess) {
    if (isLoading || !currentRoundId) return;
    setInputLoading(true);

    try {
        const res = await fetch('/api/guess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ round_id: currentRoundId, guess }),
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `HTTP ${res.status}`);
        }

        const data = await res.json();
        handleGuessResult(data, guess);
    } catch (err) {
        console.error('Guess failed:', err);
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
    // Prompt
    els.promptText.textContent = data.prompt;

    // Badges
    renderSourceBadge(data.source_type);
    els.categoryBadge.textContent = formatCategory(data.category);

    // Board
    renderBoard(data.board);

    // Stats
    renderScore(data.score);
    renderStrikes(data.strikes);

    // Clear guess history
    els.guessList.innerHTML = '';

    // Hide overlay
    hideRoundOver();

    // Enable input
    els.guessInput.disabled = false;
    els.submitBtn.disabled = false;
    els.guessInput.focus();
}

function renderBoard(slots) {
    els.answerBoard.innerHTML = '';
    slots.forEach((slot) => {
        const el = createSlotElement(slot);
        els.answerBoard.appendChild(el);
    });
}

function createSlotElement(slot) {
    const div = document.createElement('div');
    div.className = `answer-slot ${slot.revealed ? 'slot-revealed' : 'slot-hidden'}`;
    div.dataset.rank = slot.rank;

    div.innerHTML = `
        <div class="slot-rank">${slot.rank}</div>
        <div class="slot-content">${slot.revealed ? escapeHtml(slot.text) : '• • •'}</div>
        <div class="slot-score">${slot.revealed ? slot.score : '—'}</div>
    `;

    return div;
}

function renderScore(score) {
    els.scoreDisplay.textContent = score;
    els.scoreDisplay.classList.remove('flash-correct');
    void els.scoreDisplay.offsetWidth; // force reflow
    els.scoreDisplay.classList.add('flash-correct');
}

function renderStrikes(strikes) {
    const xs = els.strikesDisplay.querySelectorAll('.strike-x');
    xs.forEach((x, i) => {
        if (i < strikes) {
            if (!x.classList.contains('active')) {
                x.classList.add('active');
            }
        } else {
            x.classList.remove('active');
        }
    });
}

function renderSourceBadge(sourceType) {
    els.sourceBadge.textContent = sourceType.toUpperCase();
    els.sourceBadge.className = 'badge';
    if (sourceType === 'real') els.sourceBadge.classList.add('badge-real');
    else if (sourceType === 'ai') els.sourceBadge.classList.add('badge-ai');
    else els.sourceBadge.classList.add('badge-hybrid');
}

function addGuessToHistory(guess, correct, matchedAnswer) {
    const li = document.createElement('li');
    li.className = `guess-item ${correct ? 'correct' : 'incorrect'}`;
    const icon = correct ? '✓' : '✕';
    let text = escapeHtml(guess);
    if (correct && matchedAnswer && matchedAnswer.toLowerCase() !== guess.toLowerCase()) {
        text += ` → ${escapeHtml(matchedAnswer)}`;
    }
    li.innerHTML = `<span>${icon}</span> ${text}`;
    els.guessList.appendChild(li);
    // Scroll to bottom
    els.guessList.scrollTop = els.guessList.scrollHeight;
}


// ===========================================================================
// GUESS RESULT HANDLING
// ===========================================================================

function handleGuessResult(data, guess) {
    // Update board
    renderBoard(data.board);
    renderScore(data.score);
    renderStrikes(data.strikes);

    // Add to history
    addGuessToHistory(guess, data.correct, data.matched_answer);

    // Flash feedback on input
    if (data.correct) {
        els.guessInput.classList.add('flash-correct');
        setTimeout(() => els.guessInput.classList.remove('flash-correct'), 500);
    } else {
        els.guessInput.classList.add('flash-incorrect');
        setTimeout(() => els.guessInput.classList.remove('flash-incorrect'), 500);
    }

    // Round over?
    if (data.round_over) {
        showRoundOver(data);
    }
}


// ===========================================================================
// ROUND OVER
// ===========================================================================

async function showRoundOver(data) {
    // Disable input
    els.guessInput.disabled = true;
    els.submitBtn.disabled = true;

    // Get full revealed board
    const revealData = await revealBoard();

    // Build overlay
    const allRevealed = data.board.every(s => s.revealed);
    if (allRevealed) {
        els.overlayTitle.textContent = '🎉 Perfect Round!';
    } else if (data.strikes >= maxStrikes) {
        els.overlayTitle.textContent = '😬 Struck Out!';
    } else {
        els.overlayTitle.textContent = 'Round Over!';
    }

    // Render final board
    if (revealData) {
        els.finalBoard.innerHTML = '';
        revealData.board.forEach(slot => {
            els.finalBoard.appendChild(createSlotElement(slot));
        });
        els.finalScore.textContent = revealData.score;
        els.finalStrikes.textContent = `${revealData.strikes} / ${maxStrikes}`;

        if (revealData.commentary) {
            els.commentary.textContent = revealData.commentary;
            els.commentary.classList.remove('hidden');
        }
    } else {
        els.finalScore.textContent = data.score;
        els.finalStrikes.textContent = `${data.strikes} / ${maxStrikes}`;
    }

    els.roundOverOverlay.classList.remove('hidden');
}

function hideRoundOver() {
    els.roundOverOverlay.classList.add('hidden');
    els.commentary.classList.add('hidden');
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
    if (loading) {
        els.submitBtn.textContent = '...';
    } else {
        els.submitBtn.textContent = 'Guess';
    }
}

function clearInput() {
    els.guessInput.value = '';
    els.guessInput.focus();
}

function showError(message) {
    // Simple inline error — could enhance with toast later
    console.error(message);
    const existing = document.querySelector('.error-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        background: var(--color-danger); color: white; padding: 0.75rem 1.5rem;
        border-radius: var(--radius-md); font-size: 0.875rem; z-index: 300;
        animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function formatCategory(cat) {
    if (!cat) return 'General';
    return cat.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
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
    startNewRound(window.__INITIAL_CATEGORY__);
}
