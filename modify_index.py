import re

with open('app/templates/main/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# CSS Replacement
new_css = """
/* NEW HERO STYLES */
:root {
    --hero-bg: #050816;
    --hero-glow-blue: rgba(56, 189, 248, 0.4);
    --hero-glow-purple: rgba(139, 92, 246, 0.4);
    --hero-glow-cyan: rgba(34, 211, 238, 0.4);
}
body {
    background-color: var(--hero-bg) !important;
    color: white !important;
}

.hero-redesign {
    position: relative;
    width: 100%;
    min-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 6rem 2rem 4rem;
    font-family: 'Inter', sans-serif;
    color: white;
}

.hero-bg {
    position: absolute;
    inset: 0;
    z-index: 0;
    background: #050816;
    overflow: hidden;
}

.hero-noise {
    position: absolute;
    inset: 0;
    background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
    opacity: 0.05;
    pointer-events: none;
}

.hero-grid {
    position: absolute;
    inset: 0;
    background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
    animation: gridMove 20s linear infinite;
    pointer-events: none;
}
@keyframes gridMove {
    0% { transform: perspective(500px) rotateX(60deg) translateY(0) translateZ(-200px); }
    100% { transform: perspective(500px) rotateX(60deg) translateY(50px) translateZ(-200px); }
}

.orb-blue {
    position: absolute; top: 10%; left: 20%; width: 500px; height: 500px;
    background: radial-gradient(circle, var(--hero-glow-blue) 0%, transparent 70%);
    filter: blur(80px); animation: orbFloat 15s infinite alternate ease-in-out;
}
.orb-purple {
    position: absolute; bottom: 10%; right: 20%; width: 600px; height: 600px;
    background: radial-gradient(circle, var(--hero-glow-purple) 0%, transparent 70%);
    filter: blur(100px); animation: orbFloatRev 18s infinite alternate ease-in-out;
}

.hero-content-wrapper {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    max-width: 1400px;
    gap: 4rem;
}

.hero-left {
    flex: 1;
    max-width: 650px;
    text-align: left;
}
.hero-heading {
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}
.gradient-text-neon {
    background: linear-gradient(135deg, #38bdf8, #8b5cf6, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(56, 189, 248, 0.4);
}
.hero-subheading {
    font-size: 1.25rem;
    color: #9ca3af;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}
.hero-buttons {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 3rem;
}
.hero-buttons .btn {
    padding: 1rem 2rem;
    border-radius: 24px;
    font-size: 1.1rem;
    font-weight: 600;
}
.hero-buttons .btn-primary {
    background: linear-gradient(135deg, #38bdf8, #8b5cf6);
    color: white;
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    border: none;
}
.hero-buttons .btn-secondary {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
}
.hero-trust {
    display: flex;
    gap: 2rem;
    align-items: center;
    flex-wrap: wrap;
}
.trust-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #d1d5db;
    background: rgba(255,255,255,0.03);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.05);
}
.trust-badge .stars { color: #fbbf24; letter-spacing: 2px; }
.trust-badge i { width: 18px; color: #38bdf8; }

.hero-right {
    flex: 1;
    position: relative;
    height: 600px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1200px;
    transform-style: preserve-3d;
}

.laptop {
    position: relative;
    width: 500px;
    height: 300px;
    transform: rotateX(15deg) rotateY(-15deg);
    transform-style: preserve-3d;
    z-index: 5;
    animation: floatLaptop 6s ease-in-out infinite;
}
@keyframes floatLaptop {
    0%, 100% { transform: rotateX(15deg) rotateY(-15deg) translateY(0); }
    50% { transform: rotateX(15deg) rotateY(-15deg) translateY(-20px); }
}
.laptop-screen {
    position: absolute;
    width: 100%;
    height: 100%;
    background: #0B1220;
    border-radius: 12px;
    border: 4px solid #1f2937;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 30px rgba(56, 189, 248, 0.2);
    overflow: hidden;
}
.laptop-base {
    position: absolute;
    bottom: -15px;
    left: -5%;
    width: 110%;
    height: 15px;
    background: #374151;
    border-radius: 0 0 12px 12px;
    transform: translateZ(-10px);
}
.dashboard-ui {
    width: 100%;
    height: 100%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(139,92,246,0.1));
}
.dash-header { height: 20px; width: 100%; display: flex; gap: 0.5rem; }
.dash-dot { width: 10px; height: 10px; border-radius: 50%; background: #4b5563; }
.dash-content { flex: 1; background: rgba(255,255,255,0.05); border-radius: 8px; padding: 1rem; display: flex; gap: 1rem; }
.dash-sidebar { width: 30%; height: 100%; background: rgba(255,255,255,0.05); border-radius: 4px; }
.dash-main { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.dash-line { height: 10px; background: rgba(255,255,255,0.1); border-radius: 4px; width: 100%; }
.dash-line.short { width: 60%; }

.floating-doc {
    position: absolute;
    background: rgba(17, 24, 39, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 1rem;
    border-radius: 16px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    z-index: 10;
}
.floating-doc i { width: 24px; height: 24px; color: #38bdf8; }
.doc-pdf { top: 10%; right: -10%; animation: floatDoc 7s infinite ease-in-out; }
.doc-docx { bottom: 20%; left: -10%; animation: floatDocRev 8s infinite ease-in-out; }
.doc-txt { top: 40%; right: 110%; animation: floatDoc 9s infinite ease-in-out; }

.robot-assistant {
    position: absolute;
    top: -10%;
    left: 20%;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #38bdf8, #8b5cf6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
    z-index: 10;
    animation: bounceBot 4s infinite ease-in-out;
}
.robot-assistant i { color: white; width: 30px; height: 30px; }

.holographic-ring {
    position: absolute;
    border-radius: 50%;
    border: 2px solid rgba(56, 189, 248, 0.3);
    border-top-color: #38bdf8;
    z-index: 1;
}
.ring-1 { width: 400px; height: 400px; top: 100px; left: 50px; animation: spinRing 20s linear infinite; }
.ring-2 { width: 500px; height: 500px; top: 50px; left: 0; animation: spinRingRev 25s linear infinite; border: 1px dashed rgba(139, 92, 246, 0.4); border-bottom-color: #8b5cf6; }

.glass-widget {
    position: absolute;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.9rem;
    z-index: 15;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
.widget-grammar { bottom: -5%; right: 10%; animation: floatDoc 8s infinite ease-in-out; }
.widget-ocr { top: 30%; right: -20%; animation: floatDocRev 7.5s infinite ease-in-out; }
.highlight-error { color: #ef4444; background: rgba(239, 68, 68, 0.1); padding: 0.2rem 0.4rem; border-radius: 4px; text-decoration: line-through; }
.highlight-correct { color: #10b981; background: rgba(16, 185, 129, 0.1); padding: 0.2rem 0.4rem; border-radius: 4px; }

.shield-icon { position: absolute; top: 50%; left: -20%; color: #10b981; filter: drop-shadow(0 0 15px #10b981); z-index: 10; animation: pulseGlow 2s infinite; }
.shield-icon i { width: 40px; height: 40px; }
.ai-chip { position: absolute; bottom: 30%; left: 40%; color: #38bdf8; filter: drop-shadow(0 0 20px #38bdf8); z-index: 10; animation: bounceBot 5s linear infinite; }
.ai-chip i { width: 40px; height: 40px; }

/* Stats Redesign */
.stats-redesign {
    position: relative;
    z-index: 10;
    max-width: 1200px;
    margin: -3rem auto 5rem;
    padding: 0 2rem;
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
}
.stat-glass-card {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 24px;
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.stat-glass-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    opacity: 0; transition: opacity 0.3s;
}
.stat-glass-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15); border-color: rgba(56, 189, 248, 0.3); }
.stat-glass-card:hover::before { opacity: 1; }
.stat-icon-wrapper {
    width: 48px; height: 48px; border-radius: 12px; background: rgba(56,189,248,0.1);
    color: #38bdf8; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;
}
.stat-number { font-size: 2.5rem; font-weight: 800; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem; color: white; }
.stat-text { color: #9ca3af; font-size: 0.95rem; font-weight: 500; }

@keyframes spinRing { 100% { transform: rotate(360deg); } }
@keyframes spinRingRev { 100% { transform: rotate(-360deg); } }
@keyframes floatDoc { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
@keyframes floatDocRev { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(15px); } }
@keyframes bounceBot { 0%, 100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-20px) scale(1.1); } }
@keyframes pulseGlow { 0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px currentColor); } 50% { transform: scale(1.2); filter: drop-shadow(0 0 25px currentColor); } }

/* Scroll Animations & Others */
.scroll-animate {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
    filter: blur(10px);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.scroll-animate.show {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
}
.sparkle, .glitter {
    position: absolute; border-radius: 50%; background: white; pointer-events: none; opacity: 0;
}
.sparkle { box-shadow: 0 0 8px 2px rgba(255,255,255,0.8); animation: twinkle 3s infinite ease-in-out; width: 3px; height: 3px; }
.glitter { animation: glitterTwinkle infinite ease-in-out; }
@keyframes twinkle { 0%, 100% { opacity: 0; transform: scale(0.5); } 50% { opacity: 1; transform: scale(1.2); } }
@keyframes glitterTwinkle { 0%, 100% { opacity: 0; transform: scale(0); } 50% { opacity: 1; transform: scale(1); } }

@media (max-width: 1024px) {
    .hero-content-wrapper { flex-direction: column; text-align: center; }
    .hero-left { text-align: center; max-width: 100%; }
    .hero-buttons { justify-content: center; }
    .hero-trust { justify-content: center; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-right { height: 400px; width: 100%; margin-top: 2rem; }
    .laptop { width: 350px; height: 210px; }
}
@media (max-width: 600px) {
    .stats-grid { grid-template-columns: 1fr; }
    .hero-heading { font-size: 3rem; }
    .laptop { width: 280px; height: 168px; }
}
"""

new_html = """
<!-- Hero Section -->
<section class="hero-redesign parallax-container">
    <div class="hero-bg">
        <div class="hero-noise"></div>
        <div class="hero-grid"></div>
        <div class="orb-blue"></div>
        <div class="orb-purple"></div>
        <div id="sparkle-container"></div>
        <div id="glitter-container"></div>
    </div>

    <div class="hero-content-wrapper">
        <!-- Left Side: Content -->
        <div class="hero-left">
            <h1 class="hero-heading scroll-animate">
                AI-Powered <br>
                <span class="gradient-text-neon">Document Intelligence</span>
            </h1>
            <p class="hero-subheading scroll-animate" style="transition-delay: 0.1s;">
                Transform documents instantly with AI-powered grammar correction, OCR, formatting, plagiarism detection, translation, summarization and professional rewriting.
            </p>
            <div class="hero-buttons scroll-animate" style="transition-delay: 0.2s;">
                <a href="{{ url_for('auth.register') }}" class="btn btn-primary magnetic-btn ripple-btn">
                    Get Started Free <i data-lucide="arrow-right"></i>
                </a>
                <a href="#live-demo" class="btn btn-secondary magnetic-btn ripple-btn">
                    <i data-lucide="play-circle"></i> Watch Demo
                </a>
            </div>
            <div class="hero-trust scroll-animate" style="transition-delay: 0.3s;">
                <div class="trust-badge">
                    <div class="stars">★★★★★</div>
                    <span>Rated 4.9/5</span>
                </div>
                <div class="trust-badge">
                    <i data-lucide="file-check"></i>
                    <span>10000+ Documents Processed</span>
                </div>
                <div class="trust-badge">
                    <i data-lucide="shield-check"></i>
                    <span>99.8% Accuracy</span>
                </div>
            </div>
        </div>

        <!-- Right Side: 3D Scene -->
        <div class="hero-right">
            <div class="scene-3d">
                <div class="laptop parallax-layer" data-speed="0.02">
                    <div class="laptop-screen">
                        <div class="dashboard-ui">
                            <div class="dash-header">
                                <div class="dash-dot" style="background:#ef4444"></div>
                                <div class="dash-dot" style="background:#f59e0b"></div>
                                <div class="dash-dot" style="background:#10b981"></div>
                            </div>
                            <div class="dash-content">
                                <div class="dash-sidebar">
                                    <div class="dash-line" style="margin-bottom:1rem"></div>
                                    <div class="dash-line short" style="margin-bottom:0.5rem"></div>
                                    <div class="dash-line short" style="margin-bottom:0.5rem"></div>
                                    <div class="dash-line" style="margin-bottom:0.5rem"></div>
                                </div>
                                <div class="dash-main">
                                    <div class="dash-line" style="width:80%"></div>
                                    <div class="dash-line"></div>
                                    <div class="dash-line" style="width:90%"></div>
                                    <div class="dash-line short"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="laptop-base"></div>
                </div>

                <!-- Floating Elements -->
                <div class="floating-doc doc-pdf parallax-layer" data-speed="0.06">
                    <i data-lucide="file-text"></i> PDF
                </div>
                <div class="floating-doc doc-docx parallax-layer" data-speed="0.04">
                    <i data-lucide="file-text"></i> DOCX
                </div>
                <div class="floating-doc doc-txt parallax-layer" data-speed="0.08">
                    <i data-lucide="file-text"></i> TXT
                </div>
                <div class="robot-assistant parallax-layer" data-speed="0.05">
                    <i data-lucide="bot"></i>
                </div>
                <div class="holographic-ring ring-1 parallax-layer" data-speed="0.01"></div>
                <div class="holographic-ring ring-2 parallax-layer" data-speed="-0.01"></div>
                
                <div class="glass-widget widget-grammar parallax-layer" data-speed="0.03">
                    <div class="highlight-error">stratergy</div> <i data-lucide="arrow-right" style="width:14px"></i> <div class="highlight-correct">strategy</div>
                </div>
                <div class="glass-widget widget-ocr parallax-layer" data-speed="0.07">
                    <i data-lucide="scan-line" style="color:#38bdf8"></i> OCR Active
                </div>
                
                <div class="shield-icon parallax-layer" data-speed="0.09">
                    <i data-lucide="shield-check"></i>
                </div>
                <div class="ai-chip parallax-layer" data-speed="0.05">
                    <i data-lucide="cpu"></i>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Bottom Stats -->
<section class="stats-redesign">
    <div class="stats-grid">
        <div class="stat-glass-card scroll-animate">
            <div class="stat-icon-wrapper"><i data-lucide="files"></i></div>
            <div class="stat-number animate-counter" data-target="10000" data-suffix="+">0</div>
            <div class="stat-text">Documents Corrected</div>
        </div>
        <div class="stat-glass-card scroll-animate" style="transition-delay: 0.1s;">
            <div class="stat-icon-wrapper"><i data-lucide="check-circle-2"></i></div>
            <div class="stat-number animate-counter" data-target="99.8" data-decimal="true" data-suffix="%">0%</div>
            <div class="stat-text">Correction Accuracy</div>
        </div>
        <div class="stat-glass-card scroll-animate" style="transition-delay: 0.2s;">
            <div class="stat-icon-wrapper"><i data-lucide="globe-2"></i></div>
            <div class="stat-number animate-counter" data-target="100" data-suffix="+">0</div>
            <div class="stat-text">Languages Supported</div>
        </div>
        <div class="stat-glass-card scroll-animate" style="transition-delay: 0.3s;">
            <div class="stat-icon-wrapper"><i data-lucide="sparkles"></i></div>
            <div class="stat-number animate-counter" data-target="50" data-suffix="+">0</div>
            <div class="stat-text">AI Analysis Features</div>
        </div>
    </div>
</section>
"""

# Replace CSS
css_start = content.find("/* Premium Aurora & Sparkles */")
css_end = content.find("/* FAQ Accordion */")
if css_start != -1 and css_end != -1:
    content = content[:css_start] + new_css + "\n" + content[css_end:]

# Replace HTML
html_start = content.find("<!-- Hero Section -->")
html_end = content.find("<!-- Feature Grid Section -->")
if html_start != -1 and html_end != -1:
    content = content[:html_start] + new_html + "\n" + content[html_end:]

with open('app/templates/main/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Update complete")
