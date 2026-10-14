/* ==========================================================================
   PALGRIMIZER INTERACTIVE DIFF STUDIO LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const docIdElement = document.getElementById('documentId');
    if (!docIdElement) return;

    const docId = docIdElement.value;
    const viewModeBtns = document.querySelectorAll('.mode-btn');
    const sideBySideView = document.getElementById('sideBySideView');
    const inlineDiffView = document.getElementById('inlineDiffView');

    // 1. Side-by-side vs Inline View Mode Switcher
    viewModeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            viewModeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const mode = btn.getAttribute('data-mode');
            if (mode === 'inline') {
                if (sideBySideView) sideBySideView.style.display = 'none';
                if (inlineDiffView) inlineDiffView.style.display = 'block';
            } else {
                if (inlineDiffView) inlineDiffView.style.display = 'none';
                if (sideBySideView) sideBySideView.style.display = 'grid';
            }
        });
    });

    // 2. Accept / Reject Individual Suggestion Actions
    document.querySelectorAll('.accept-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const corrId = btn.getAttribute('data-corr-id');
            btn.disabled = true;

            try {
                const res = await fetch(`/api/document/${docId}/accept-correction`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ correction_id: corrId })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    const card = document.getElementById(`suggestion-card-${corrId}`);
                    if (card) {
                        card.style.opacity = '0.5';
                        card.style.pointerEvents = 'none';
                        card.querySelector('.suggestion-actions').innerHTML = '<span class="badge badge-success"><i class="fas fa-check"></i> Accepted</span>';
                    }
                    updateOverallScore(data.new_score);
                    window.showToast('Suggestion accepted.', 'success');
                }
            } catch (err) {
                window.showToast('Action failed.', 'danger');
            }
        });
    });

    document.querySelectorAll('.reject-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const corrId = btn.getAttribute('data-corr-id');
            btn.disabled = true;

            try {
                const res = await fetch(`/api/document/${docId}/reject-correction`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ correction_id: corrId })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    const card = document.getElementById(`suggestion-card-${corrId}`);
                    if (card) {
                        card.style.opacity = '0.5';
                        card.style.pointerEvents = 'none';
                        card.querySelector('.suggestion-actions').innerHTML = '<span class="badge badge-danger"><i class="fas fa-times"></i> Rejected</span>';
                    }
                    window.showToast('Suggestion rejected.', 'info');
                }
            } catch (err) {
                window.showToast('Action failed.', 'danger');
            }
        });
    });

    // 3. Apply All Corrections
    const applyAllBtn = document.getElementById('applyAllCorrectionsBtn');
    if (applyAllBtn) {
        applyAllBtn.addEventListener('click', async () => {
            applyAllBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Applying All...';
            try {
                const res = await fetch(`/api/document/${docId}/apply-all`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await res.json();
                if (data.status === 'success') {
                    updateOverallScore(data.new_score);
                    document.querySelectorAll('.suggestion-card').forEach(card => {
                        card.style.opacity = '0.5';
                        card.style.pointerEvents = 'none';
                        const actions = card.querySelector('.suggestion-actions');
                        if (actions) actions.innerHTML = '<span class="badge badge-success"><i class="fas fa-check"></i> Accepted</span>';
                    });
                    window.showToast('All AI corrections applied successfully!', 'success');
                }
            } catch (err) {
                window.showToast('Failed to apply all corrections.', 'danger');
            } finally {
                applyAllBtn.innerHTML = '<i class="fas fa-check-double"></i> Apply All Corrections';
            }
        });
    }

    // Helper to update Score Ring Gauge
    function updateOverallScore(newScore) {
        const scoreVal = document.getElementById('overallScoreText');
        const scoreCircle = document.getElementById('overallScoreCircle');
        if (scoreVal) scoreVal.innerText = newScore + '%';
        if (scoreCircle) {
            const offset = 283 - (283 * (newScore / 100));
            scoreCircle.style.strokeDashoffset = offset;
        }
    }
});
