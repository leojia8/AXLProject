/**
 * game.js — Client-Side Game Controller
 *
 * Responsibilities:
 * - Initialize game on page load (fetch new round or resume)
 * - Handle guess submission (input + button + Enter key)
 * - Call API endpoints via fetch() and update DOM
 * - Render/update the answer board (hidden → revealed transitions)
 * - Update score and strikes display
 * - Manage guess history list
 * - Show/hide round-over overlay
 * - Handle loading states during API calls
 * - "New Round" / "Play Again" button logic
 *
 * Architecture:
 * - All state comes from the server via API responses
 * - Client renders state — does NOT store answers
 * - Input is disabled during API calls to prevent double-submit
 *
 * API calls:
 * - POST /api/new-round   → start fresh round
 * - POST /api/guess        → submit a guess
 * - POST /api/reveal       → reveal full board
 * - GET  /api/categories   → populate category selector
 */


// ===========================================================================
// STATE
// ===========================================================================

// TODO: let currentRoundId = null;
// TODO: let isLoading = false;


// ===========================================================================
// DOM REFERENCES
// ===========================================================================

// TODO: Cache DOM element references on load
// - promptArea, answerBoard, inputField, submitBtn
// - scoreDisplay, strikesDisplay
// - guessHistory, roundOverOverlay, loadingSpinner
// - newRoundBtn, playAgainBtn, categorySelect


// ===========================================================================
// INITIALIZATION
// ===========================================================================

// TODO: document.addEventListener('DOMContentLoaded', init)
// TODO: function init()
//   - Attach event listeners (submit btn, Enter key, new round btn)
//   - Optionally load categories
//   - Start first round automatically


// ===========================================================================
// API CALLS
// ===========================================================================

// TODO: async function startNewRound(category = null)
//   - POST /api/new-round with { category, prefer_real: true }
//   - On success: store round_id, render board, reset UI
//   - On error: show error message

// TODO: async function submitGuess(guess)
//   - Validate input (non-empty, not duplicate)
//   - POST /api/guess with { round_id, guess }
//   - On success: update board, score, strikes, guess history
//   - If correct: play reveal animation
//   - If incorrect: play strike animation
//   - If round_over: show round-over overlay

// TODO: async function revealBoard()
//   - POST /api/reveal with { round_id }
//   - Show full board in overlay


// ===========================================================================
// RENDERING
// ===========================================================================

// TODO: function renderBoard(boardSlots)
//   - Clear existing board
//   - For each slot: create DOM element
//   - Hidden slots: show rank number + "???"
//   - Revealed slots: show rank + answer text + score
//   - Apply reveal animation class for newly revealed slots

// TODO: function renderScore(score)
//   - Update score display with animation

// TODO: function renderStrikes(strikes, maxStrikes)
//   - Show filled/unfilled X marks
//   - Shake animation on new strike

// TODO: function addGuessToHistory(guess, correct, matchedAnswer)
//   - Append to guess history list
//   - Color code: green for correct, red for incorrect

// TODO: function showRoundOver(revealData)
//   - Show overlay with full board
//   - Display final score
//   - Optional: show commentary
//   - Show "Play Again" button

// TODO: function hideRoundOver()
//   - Hide overlay, reset for new round


// ===========================================================================
// UI HELPERS
// ===========================================================================

// TODO: function setLoading(loading)
//   - Show/hide spinner
//   - Enable/disable input + buttons

// TODO: function clearInput()
//   - Clear guess input and refocus

// TODO: function showError(message)
//   - Briefly show an error toast/message


// ===========================================================================
// EVENT HANDLERS
// ===========================================================================

// TODO: function handleSubmit(e)
//   - Prevent default
//   - Get input value
//   - Call submitGuess()
//   - Clear input

// TODO: function handleKeyPress(e)
//   - If Enter key, trigger submit

// TODO: function handleNewRound()
//   - Get selected category (if any)
//   - Call startNewRound()
