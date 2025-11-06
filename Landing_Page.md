# 📚 PLAYBOOK 1: Foundation & Research
## Days 0-1 | Build Market Intelligence
### Step 1.1: Deep Customer Understanding
Objective: Create personas that reveal psychological triggers, not just demographics.
LLM Prompt:
```
Build 3 detailed personas for {product}. For each persona include:
- Demographics & role
- Top 3 pain points (emotional + practical)
- Desired outcomes (what success looks like)
- Must-have features vs nice-to-haves
- Buying triggers (what makes them act NOW)
- Top 3 objections (what stops them from buying)
- Exact language they use (phrases, metaphors)
- Where they hang out online
- Top 7 objections with plain-language quotes


Enhanced LLM Prompt for Step 1.1 (Deep Customer Understanding)
Context: I’m building {your product or service description}. You are an AI market‑research analyst. Use proven persona‑building frameworks to create three detailed buyer personas for this product.
For each persona, include:
.Identity & Demographics: Assign a realistic name, age range, role and key demographic details (occupation, location, education, income etc.)
.Psychographics & Behaviors: Describe their values, interests, lifestyle and personality traits, along with typical online/offline behaviors and the communities or social platforms where they spend time
discovercrisp.com
delve.ai
.Needs & Goals: Outline their functional goals (what they need to accomplish) and emotional goals (why fulfilling these goals matters to them)
discovercrisp.com
, including long‑term ambitions
.Job(s) to Be Done: Explain the underlying “job” they are hiring this product to do – i.e., the outcome they seek and the context in which they need it
delve.ai
.Challenges & Pain Points: List specific problems, sources of frustration and the impact on their life that your product must address
discovercrisp.com
persona.qcri.org
.Buying Triggers: Identify psychological, cognitive and identity triggers (e.g., urgency, scarcity, social proof, fear of missing out) that would prompt them to act now
m1-project.com
.Loss Aversion & Status Quo: Describe what they fear losing by not solving the problem and why they haven’t solved it already (status‑quo bias).
Must‑Have Features vs Nice‑to‑Haves: Differentiate between essential and optional features for this persona.
Objections & Quotes: Give the top three objections that might stop them from buying, with example quotes in their own words.
Language & Channels: Provide exact phrases, metaphors or social‑media posts they might use when discussing this problem, and list where they research solutions (blogs, communities, influencers, etc.)
discovercrisp.com
.Decision Process: Summarize their decision‑making process: how they gather information, evaluate options and what factors influence their final choice
discovercrisp.com
.Brief Narrative: Conclude with a short narrative that brings the persona to life and highlights their motivations, frustrations and aspirations.
Deliverable: Provide three complete persona documents, each clearly separated, using clear and empathetic language.
```

**What you're extracting:**
- **Jobs-to-be-Done:** What "job" are they hiring your product for?
- **Loss aversion points:** What are they afraid of losing?
- **Status quo bias:** Why haven't they solved this already?

**Output:** 3 persona documents with psychological profiles

---

### **Step 1.2: Competitor Intelligence**

**Objective:** Reverse-engineer what works, identify gaps, generate testable hypotheses.

**LLM Prompt:**
```
Analyze these 5 competitor landing pages: {URLs}

For each, extract:
1. Core value proposition (exact headline)
2. CTA strategy (primary/secondary, placement, copy)
3. Pricing psychology (tiers, anchoring, framing)
4. Social proof tactics (testimonials, logos, numbers)
5. Objections they address (and how)
6. Trust-building elements (guarantees, security)
7. Visual hierarchy and flow
8. What's missing or weak

Then synthesize:
- 10 testable hypotheses I can implement
- 3 differentiation opportunities
- Pricing strategies ranked by effectiveness



Enhanced LLM Prompt for Step 1.2 (Competitor Intelligence)
Context: I’m assessing up to five competitor landing pages for {product/industry}. You are a conversion‑rate optimization analyst. Use landing‑page research and behavioural psychology to reverse‑engineer each page.
For each competitor URL, extract and evaluate:
Core value proposition: Quote the exact headline/tagline that communicates the offer.
CTA strategy: Identify the primary and secondary calls‑to‑action (CTAs), note their placement (e.g., above the fold, mid‑page, end), and describe the copy and design (button text, colour, contrast). Best practice is to have the main CTA visible above the fold and repeated for long pages
unbounce.com
.
Pricing psychology: Describe how pricing is framed. Note any tiers, decoy effect, anchoring (showing a higher price before the real price) or discount displays
serotonin.co.uk
. Highlight scarcity or loss‑aversion tactics such as limited‑time offers or guarantees
serotonin.co.uk
serotonin.co.uk
.
Social proof: List testimonials, user counts, star ratings or logos used to build trust
serotonin.co.uk
. Assess whether the proof is specific (includes names, roles, metrics).
Objections addressed: Identify customer objections or pain points mentioned and explain how the page counters them.
Trust‑building elements: Point out trust signals such as money‑back guarantees, secure checkout badges, certifications or free trials
webstacks.com
.
Visual hierarchy and flow: Describe how the design guides the visitor’s eye—headline prominence, CTA contrast, use of whitespace and logical progression
serotonin.co.uk
.
Missing or weak elements: Note gaps such as lack of CTA above the fold, vague value proposition, weak social proof or absent trust signals.
After reviewing all pages, synthesise your insights:
Competitor analysis matrix: Create a table summarising strengths, weaknesses and notable tactics for each competitor across the above criteria.
10 testable hypotheses: Propose actionable experiments for my landing page based on observed patterns (e.g., adding scarcity messages, repositioning CTAs, improving trust signals).
3 differentiation opportunities: Suggest unique value propositions or messaging angles that competitors are not using.
Rank pricing strategies: Compare the psychological effectiveness of each competitor’s pricing structure (decoy tiers, anchoring, savings framing) and rank them.
Guidance: When making recommendations, reference relevant psychological principles such as social proof, scarcity/FOMO, anchoring, loss aversion, reciprocity and visual hierarchy
serotonin.co.uk
serotonin.co.uk
serotonin.co.uk
. Provide clear, actionable analysis and present hypotheses and differentiation ideas in complete sentences.
```

**I will use `web_search` and `web_fetch` to:**
- Find top-converting landing pages in your industry
- Analyze their structure and copy
- Extract patterns you can adapt

**Output:** Competitor analysis matrix + 10 hypotheses to test

---

### **Step 1.3: Cross-Industry Inspiration**

**Objective:** Import proven conversion tactics from industries that have mastered specific problems.

**What to look for:**
- **SaaS (Stripe, Notion):** Free trial CTAs, product-led demos
- **E-commerce (Amazon, Shopify):** Scarcity, urgency, social proof
- **Fintech (Revolut, Wise):** Trust-building, security messaging
- **B2B (Salesforce, HubSpot):** ROI calculators, case studies
- **Creator economy (Gumroad, Teachable):** Founder story, mission-driven

**LLM Prompt:**
```
Search for the highest-converting landing pages in {industry}. 
For the top 3, analyze:
- What conversion principle they've mastered
- How they reduce friction
- Their unique psychological trigger
- How I can adapt this to {my product/market}

Enhanced LLM Prompt for Step 1.3 (Cross‑Industry Inspiration)
Context: I’m looking for proven conversion tactics from outside my sector to inspire my landing page. You are a conversion expert with access to public web data.
Select up to three of the highest‑converting landing pages in {industry}. Prioritize pages that rank highly for conversions or are widely recognized for excellence. Be specific about the URL/company.
For each page, report on four areas:
Dominant conversion principle: Identify the main tactic driving conversion (e.g., free trial & demo flow in SaaS
serotonin.co.uk
, scarcity & urgency banners in e‑commerce
leadpages.com
, trust/security messaging in fintech
webstacks.com
, ROI calculators & case studies in B2B
muffingroup.com
muffingroup.com
, founder story & mission in creator economy
newbeach.co
). Explain how it’s implemented on the page (e.g., placement, copy tone, visuals).
Friction‑reduction tactics: Describe how the page removes barriers—such as prominent CTAs above the fold and repeated down the page
unbounce.com
, simplified forms
muffingroup.com
, or free trials/guarantees
serotonin.co.uk
.
Unique psychological trigger: Identify the cognitive bias or emotion employed—social proof (customer logos, testimonials)
serotonin.co.uk
; scarcity/FOMO through limited‑time offers
serotonin.co.uk
; loss‑aversion framing (emphasizing what users lose by not acting)
serotonin.co.uk
; anchoring/decoy pricing
serotonin.co.uk
; reciprocity via free resources
serotonin.co.uk
; founder story/personal narrative
newbeach.co
, etc. Quote or paraphrase any notable copy.
Adaptation ideas for {my product/market}: Suggest one or two ways to translate the tactic to my product. For example, if a fintech page uses security badges and compliance certifications to build trust
webstacks.com
, recommend equivalent trust signals for my product. If a B2B page features an interactive ROI calculator
muffingroup.com
, propose a simple ROI or savings estimator relevant to my offering.
Deliverable: Present a concise report summarizing the three pages, each with the four sections above. End with a bullet list of 3–5 cross‑industry tactics you believe could be most impactful for my product, explaining why each is promising.


```

**Output:** 3-5 transferable tactics with implementation ideas

---

### **Step 1.4: Research-Backed Conversion Principles**

**Objective:** Ground every design decision in behavioral science.

**Core Frameworks to Apply:**

#### **A. Cialdini's 6 Principles of Persuasion**
1. **Reciprocity:** Give value before asking (free tool, guide, assessment)
2. **Scarcity:** Limited spots, time-bound offers, inventory counts
3. **Authority:** Expert endorsements, credentials, media mentions
4. **Consistency:** Small commitments first (quiz → email → purchase)
5. **Liking:** Shared values, founder story, relatable brand voice
6. **Social Proof:** Customer count, testimonials, case studies with specifics

#### **B. BJ Fogg's Behavior Model**
**Formula:** Motivation + Ability + Trigger = Action

- **Motivation:** Amplify pain, show outcome clearly
- **Ability:** Reduce friction (fewer fields, one-click options)
- **Trigger:** Clear, action-oriented CTAs at the right moment

#### **C. Loss Aversion (Kahneman & Tversky)**
People are 2x more motivated to avoid loss than gain something.

**Applications:**
- "Don't miss out on {outcome}" > "Get {outcome}"
- "Without this, you'll keep {pain}" > "This gives you {benefit}"
- Risk-reversal guarantees

#### **D. Eye-Tracking Patterns**
- **F-pattern:** Users scan left to right at top, then vertically down left side
- **Z-pattern:** For simpler pages (zigzag: top-left → top-right → bottom-left → bottom-right)
- **Above the fold:** 80% of attention goes here

**LLM Prompt:**
```
For this landing page structure {paste outline}, map where to apply:
- Cialdini's 6 principles (specific placements)
- Fogg triggers (at decision points)
- Loss aversion framing (exact copy suggestions)
- Eye-tracking optimization (what goes where and why)

For each principle, give exact implementation examples.


Enhanced LLM Prompt for Step 1.4 (Research‑Backed Conversion Principles)
Context: I’m designing a conversion‑focused landing page. Below is my page outline {paste outline}. You are a behavioural‑science‑informed conversion strategist.
Your tasks:
Map Cialdini’s six persuasion principles to specific sections.
Reciprocity: Suggest where to offer free value (e.g., tools, guides, assessments) before asking for commitment
people-shift.com
.
Scarcity: Identify moments to use limited spots, time‑bound offers or inventory counts to create urgency
people-shift.com
.
Authority: Recommend placements for expert endorsements, credentials or media logos
people-shift.com
.
Commitment/Consistency: Propose low‑friction micro‑conversions (quiz → email → purchase) to build momentum
people-shift.com
.
Liking: Indicate where to use relatable stories, shared values or founder narrative to build affinity
people-shift.com
.
Social proof: Describe how to integrate customer counts, testimonials and case study snippets
people-shift.com
.
Apply BJ Fogg’s Behaviour Model (B = MAP). Behaviour occurs when motivation, ability and a prompt converge
behaviormodel.org
. For each section, specify:
Trigger placement: Where should a call‑to‑action or prompt appear when motivation is highest and friction is lowest?
Ability enhancements: How can we simplify the action (e.g., fewer form fields, one‑click options) to increase ability?
Motivation boosters: What messaging amplifies pain or clarifies the desired outcome to raise motivation?
Embed loss‑aversion framing. People perceive losses as roughly twice as impactful as equivalent gains
behavioraleconomics.com
. Suggest copy that emphasises what users risk losing by not acting (“Don’t miss out on …” or “Without this, you’ll keep {pain}”) and recommend risk‑reversal guarantees (refunds, no‑risk trials).
Optimise for eye‑tracking patterns.
Above the fold: Users spend ~80 % of their viewing time above the fold
searchenginejournal.com
; identify which content (value proposition, social proof, primary CTA) must appear here.
Left‑side bias & F‑pattern: Users read horizontally near the top, then move down and scan along the left
searchenginejournal.com
; suggest structuring headlines, subheads and bullet lists so key information appears in the first few words
searchenginejournal.com
.
Other patterns: Note if a Z‑pattern or “layer‑cake” pattern may apply for simpler pages, and adjust layout accordingly.
For each section of the outline, produce:
Primary principle(s) applied (e.g., Social proof + Authority in the hero).
Specific copy or design element to implement the principle (e.g., “Join 2,000 founders who saved 10 hours/week” next to CTA).
Rationale linking the element to the psychological research (e.g., above‑the‑fold placement captures most attention
searchenginejournal.com
).
A/B test suggestion to experiment with variations (e.g., testing scarcity vs. social‑proof emphasis).
Deliverable: A section‑by‑section “psychological trigger map” table summarising these details, followed by 3–5 high‑level recommendations on how to sequence persuasive elements across the page.

```

**Output:** Psychological trigger map for your page

---

### **Step 1.5: Value Proposition Development**

**Objective:** Craft headlines that instantly communicate value and trigger action.

**LLM Prompt:**
```
Generate 10 headline + subhead combinations using these formulas:

Formula 1: {Primary outcome} for {ICP} without {hated thing} in {time/cost bound}
Formula 2: {Specific result} — even if {common objection}
Formula 3: The {superlative} way to {desired outcome} — {proof point}

Requirements:
- H1 must be ≤12 words
- Include specific numbers where possible
- Avoid jargon or clever wordplay
- Lead with outcome, not process

Test them against these criteria:
- Does it pass the "blink test"? (understandable in 3 seconds)
- Does it trigger FOMO or loss aversion?
- Is it specific enough to filter in the right audience?

Enhanced LLM Prompt for Step 1.5 (Value Proposition Development)
Context: I’m refining the value proposition for {product}. You are a direct‑response copywriter with expertise in conversion psychology.
Task: Generate 10 headline + subheadline pairs following the formulas below. Each pair should immediately communicate the primary benefit and motivate action.
Formulas to use:
Outcome without Obstacle: {Primary outcome} for {ICP} without {painful obstacle} in {time/cost bound}.
Result Despite Objection: {Specific result} — even if {common objection}.
Superlative Method: The {superlative} way to {desired outcome} — {proof point}.
Guidelines (based on research):
Pass the 3‑second “blink test”: Chartbeat data shows most visitors disengage within 3–5 seconds
revolutexdigital.com
, so make headlines instantly understandable.
Lead with benefits and specificity: Use concrete numbers or time frames (e.g., “Save 10 hours/week”)—this improves clarity and relevance
thrivethemes.com
.
Avoid jargon or clever wordplay: The brain prefers cognitively fluent messages
revolutexdigital.com
.
Trigger FOMO or loss aversion: Use phrases that highlight what readers risk missing out on (e.g., “Don’t miss your chance…”). FOMO creates urgency
revolutexdigital.com
 and loss aversion makes people more motivated to avoid missing benefits.
Evoke emotional resonance: Headlines that stir fear, awe, inspiration or curiosity are more clickable
revolutexdigital.com
.
Include a supporting subheadline: Use this line to clarify the offer, address a common objection, introduce urgency or social proof (e.g., “Join 5,000 creators who doubled their sales”).
For each pair, provide:
Headline (≤ 12 words) focused on the outcome.
Subheadline that expands on the promise, includes a number or social proof, and addresses a pain point or objection.
Brief rationale (1 sentence) explaining which psychological lever you used (clarity, FOMO, curiosity, social proof, loss aversion) and why.
Deliverable: A list of 10 headline + subheadline combinations with rationales.


```

**Output:** 10 value prop candidates (you'll pick top 2 to test)

---

# 📐 PLAYBOOK 2: Architecture & Psychological Mapping
## Day 2 | Design the Conversion System

### **Step 2.1: Page Architecture**

**Objective:** Build a structure that addresses objections in the right order.

**The Proven Section Order:**
```
1. HERO SECTION
   - Outcome-driven headline (≤12 words)
   - Proof nugget (social proof or authority)
   - Primary CTA (commit action: "Pre-order now")
   - Secondary CTA (lower friction: "See how it works")
   - Hero visual (product in use or aspirational outcome)

2. CREDIBILITY BAR
   - Logos of customers/partners OR
   - Numbers (X customers, Y outcome, Z rating) OR
   - Authority quote (press, expert, award)

3. PROBLEM → OUTCOME
   - 3 sentences: empathize with pain → show outcome
   - Use emotional language from personas

4. HOW IT WORKS
   - 3 steps maximum
   - Visual icons + brief descriptions
   - End with "Start now" CTA

5. BENEFITS OVER FEATURES
   - 3-5 benefits (each = outcome customer cares about)
   - For each: benefit headline + proof line + visual
   - Avoid feature lists

6. SOCIAL PROOF
   - 2-3 specific testimonials (include outcome + metric)
   - Video testimonials if available
   - Case study snippets

7. PRICING & OFFER
   - 3 tiers with decoy pricing (see Step 2.2)
   - Comparison row (who it's for, key outcome, limits)
   - Annual/monthly toggle
   - Reference price or savings shown

8. RISK REVERSAL
   - Guarantee: "100% refund if we don't ship by {date}"
   - Additional: Cancel anytime, no questions asked
   - Delivery timeline transparency

9. FAQ
   - Address top 4 objections from personas
   - Questions: "When do I get access?" "What if it's not for me?" 
     "How is payment handled?" "What if launch slips?"

10. FINAL CTA
    - Restate primary CTA
    - Add reassurance microcopy near button
    - Security badges, accepted payment methods

11. CHECKOUT
    - Minimal fields (email + payment)
    - Reassurance: "Secure checkout • Cancel anytime • Refund guaranteed"
    - Progress indicator if multi-step
```

---

### **Step 2.2: Decoy Pricing Psychology**

**Objective:** Use behavioral economics to guide users toward your target tier.

**The Decoy Effect:**
Present 3 options where the middle option is designed to look like the obvious best choice.

**Structure:**

| Tier | Price | Purpose | Features |
|------|-------|---------|----------|
| **Starter** | $29/mo | Make middle look affordable | Limited features, clear constraints |
| **Pro** ⭐ | $79/mo | **TARGET** (most profitable) | Full features + volume, "BEST VALUE" badge |
| **Enterprise** | $299/mo | **DECOY** (anchor) | Overkill for most, makes $79 feel reasonable |

**Key Tactics:**
- **Anchoring:** Show Enterprise first (resets expectations)
- **Comparison row:** "Perfect for: Solo founders / Growing teams / Large orgs"
- **Visual emphasis:** Highlight Pro with color, badge, larger card
- **Savings framing:** "Save $348/year" on annual plans

**LLM Prompt:**
```
Design 3-tier decoy pricing for {product} targeting {ICP}:
- Starter tier: baseline offering at {low price}
- Pro tier (TARGET): optimal for most at {mid price}
- Enterprise tier (DECOY): anchor at {high price}

For each tier:
- List features (what's included/excluded)
- Who it's perfect for (ICP segment)
- Key outcome they'll achieve
- Limits or constraints

Add:
- Annual discount percentage
- "Best value" positioning for Pro
- Comparison matrix format
```

**Output:** Pricing table with psychological triggers embedded

---

### **Step 2.3: Psychological Trigger Mapping**

**Objective:** Place each conversion principle at the exact right moment in the user journey.

**LLM Prompt:**
```
For this page architecture {paste structure}, create a psychological trigger map:

For each section, specify:
1. Primary psychological principle (Cialdini, Fogg, Loss Aversion)
2. Exact copy/design element to implement it
3. Why this trigger works at this moment
4. A/B test variant to try later

Example:
Section: Hero
- Principle: Social Proof (Cialdini)
- Implementation: "Join 1,247 founders already building with us"
- Why: Reduces perceived risk immediately
- Test variant: Authority instead ("Featured in TechCrunch")

Do this for all 11 sections.
```

**Enhanced LLM**
```
Context: We’ve finalised our landing‑page architecture (11 sections listed below). You are a conversion strategist trained in behavioural psychology. Use Cialdini’s persuasion principles (reciprocity, scarcity, authority, consistency/commitment, liking, social proof), Fogg’s behaviour model (motivation, ability, triggers) and loss‑aversion research (people weigh losses about twice as much as gains
behavioraleconomics.com
) to assign optimal triggers to each section.
Sections:
Hero section – outcome‑driven headline, proof nugget, primary & secondary CTAs, hero visual
Credibility bar – logos/numbers/authority quote
Problem → Outcome – 3 sentences empathising with the pain and promising a desired outcome
How it works – 3 steps, icons, “Start now” CTA
Benefits over features – 3–5 benefit statements with proof and visuals
Social proof – testimonials, metrics, case snippets
Pricing & Offer – 3 tiers with decoy pricing, comparison row, toggles
Risk reversal – guarantees, cancel‑anytime policy, transparency
FAQ – addresses four top objections
Final CTA – restated primary CTA with reassurance microcopy
Checkout – minimal form fields, reassurance and progress indicator
For each section, provide the following in a table (columns: Section, Primary Psychological Principle, Implementation, Rationale, A/B Test Variant):
Primary principle: Choose from Cialdini’s six principles, Fogg’s model (motivation, ability, trigger) or loss‑aversion. For example, the hero often uses social proof
serotonin.co.uk
; pricing uses scarcity or anchoring
serotonin.co.uk
.
Implementation: Draft a specific copy or design element that embodies this principle. For instance, in the hero you might use a statement like “Join 2 000 founders who saved 10 hours/week”
serotonin.co.uk
, or in the risk‑reversal section include “100% money‑back guarantee if we miss our ship date.”
Rationale: Explain in one sentence why this trigger works in that position. Relate it to research (e.g., social proof reduces perceived risk
serotonin.co.uk
; scarcity/FOMO accelerates decisions
serotonin.co.uk
; above‑the‑fold elements capture ~80% of attention
searchenginejournal.com
).
A/B test variant: Suggest a variation using a different principle (e.g., swap social proof for authority by citing press mentions; test loss‑aversion framing vs. benefit‑focused framing).
Guidance:
Hero section: Prioritise social proof or authority; show outcomes above the fold
serotonin.co.uk
serotonin.co.uk
.
Credibility bar: Use authority or social proof (logos, numbers) to build trust quickly
serotonin.co.uk
.
Problem → Outcome: Frame the pain and risk of inaction to tap loss aversion
serotonin.co.uk
.
How it works: Emphasise simplicity and ability by outlining a 3‑step process; Fogg’s model notes that reducing friction increases the likelihood of action
serotonin.co.uk
.
Benefits: Highlight clear outcomes and proof points; emphasise liking and reciprocity with empathetic tone
serotonin.co.uk
.
Social proof: Integrate specific testimonials with metrics
serotonin.co.uk
. A/B test authority or quantitative social proof.
Pricing & Offer: Use scarcity/decoy pricing; anchor high and highlight the “best value” plan
serotonin.co.uk
.
Risk Reversal: Tap reciprocity and commitment by offering risk‑free trials or money‑back guarantees
serotonin.co.uk
.
FAQ: Use consistency and commitment; address objections raised in personas.
Final CTA: Ensure the timing aligns with peak motivation; include Fogg’s trigger (clear action) and reassurance microcopy.
Checkout: Reduce friction—minimal fields—and include trust badges (authority and social proof).
Output: Provide a completed table for all 11 sections, followed by two overarching recommendations on sequencing (e.g., repeating CTAs after social proof) and any additional behavioural insights you think are critical for this audience.
```

**Key Trigger Placements:**

| Section | Primary Trigger | Implementation |
|---------|----------------|----------------|
| Hero | Social Proof | "X customers, Y outcome" |
| Problem | Loss Aversion | "Without this, you'll keep {pain}" |
| How It Works | Ability (Fogg) | Show how simple it is (3 steps) |
| Benefits | Outcome Focus | Specific metrics, not features |
| Social Proof | Authority + Liking | Real testimonials with photos |
| Pricing | Scarcity | "50 founding member spots left" |
| Risk Reversal | Reciprocity | Remove all perceived risk |
| FAQ | Consistency | Address objections proactively |
| Final CTA | Trigger (Fogg) | Clear action at high-motivation moment |


| Trigger (principle)                           | Where it goes                  | Copy pattern                                      | Example                                                           | Guardrail                         |
| --------------------------------------------- | ------------------------------ | ------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------- |
| **Clarity > cleverness** (processing fluency) | H1/subhead                     | Outcome → without → time/cost bound               | “Close your books in 5min — without spreadsheets — this quarter.” | No jargon; test readability       |
| **Authority**                                 | Above the fold or near pricing | Credible logos, certifications, expert pull-quote | “Trusted by CFOs at …”                                            | Real, verifiable proof only       |
| **Social proof**                              | Near CTAs & pricing            | Specific, quantified testimonials                 | “Cut AP time 43% in 30 days.”                                     | Avoid vague hype                  |
| **Scarcity/urgency**                          | Pricing & checkout             | Time-boxed or capacity-bound pilot                | “Founding plan: 50 seats until Nov 15.”                           | Use honest limits; no fake timers |
| **Risk reversal**                             | Offer & checkout               | Refund/ship guarantee, plain English              | “Instant refund if we miss Feb 10.”                               | State terms clearly               |
| **Commitment/consistency**                    | Secondary CTA                  | Low-friction step that previews value             | “See your savings in 90s (no email).”                             | Make step genuinely useful        |
| **Anchoring/decoy**                           | Pricing table                  | High anchor + best-value middle                   | “Teams €149” (anchored by “Pro €249”)                             | Ensure tiers are fair             |
| **Loss aversion**                             | Problem → Outcome              | Frame avoided risks/costs                         | “Stop paying late fees—keep €X/mo.”                               | Balance with positive gains       |
| **Reciprocity**                               | Before ask                     | Free useful artifact                              | “Download the ROI calculator.”                                    | Don’t gate everything             |


**Output:** Section-by-section trigger implementation guide

---

### **Step 2.4: Copy Optimization**

**Objective:** Write copy that sells the outcome, not the product.

**LLM Prompt:**
```
Using this architecture {paste}, personas {paste}, and trigger map {paste}, 
write full landing page copy in {brand tone: e.g., confident but empathetic}.

Requirements:
- Every section addresses a specific persona objection
- Use outcome-focused language (what they achieve, not what the product does)
- Include specific numbers and proof points
- Write decoy pricing copy with comparison matrix
- Add pre-order terms: delivery date {date}, refund policy, what's included
- Write checkout reassurance microcopy for near payment button

Sections to write:
[list all 11 sections]

For each benefit, use this formula:
"[Outcome headline] → [Proof line with metric] → [How it works in 1 sentence]"
```

**Copywriting Formulas:**

**Headlines:**
- Outcome + Audience + Without Objection: "Close deals 3x faster for B2B founders—without hiring SDRs"
- Specific Result + Time: "Ship your MVP in 30 days, not 6 months"
- Problem + Solution + Proof: "Never lose a lead again—save 47 hours/month on follow-ups"

**CTAs:**
- Primary (commit): "Start {specific outcome} now" or "Pre-order {product} — $X"
- Secondary (explore): "See exactly how it works (2-min demo)"

**Social Proof:**
- Specific: ❌ "Great product!" → ✅ "Closed 3 deals in first week—our pipeline is finally organized"
- Include outcome metric + role

**FAQ Answers:**
- Start with reassurance: "You get instant access the day we launch ({date})"
- End with guarantee: "If we don't ship on time, 100% refund—no questions asked"

**Output:** Complete page copy ready to implement

---

### **Step 2.5: Pre-Order Terms & Ethical Validation**

**Objective:** Make pre-orders feel safe, transparent, and ethical.

**Critical Elements:**
1. **What's included:** Specific features/access they're buying
2. **Delivery date:** Realistic estimate with buffer
3. **Refund policy:** "100% instant refund until {date} or if we don't ship"
4. **What happens if you're late:** "Every week late = 20% discount or instant refund"
5. **Data use:** How you'll contact them, privacy

**LLM Prompt:**
```
Draft clear, friendly pre-order terms for {product}:
- Pre-order price: {$X}
- Expected delivery: {date}
- What they get: {features list}
- Refund policy: 100% instant refund until delivery or if we miss deadline
- Late delivery consequence: {discount or bonus}
- Data use: email for updates only, no spam, unsubscribe anytime

Write in conversational tone, not legal jargon.
Also write checkout reassurance microcopy (1 sentence near payment button).
```

**Example Output:**
```
✅ Checkout Microcopy:
"Secure checkout • Instant refund if we don't ship by March 2025 • Cancel anytime"

📄 Pre-Order Terms:
Your $49 pre-order gets you:
- Full access on launch day (estimated March 15, 2025)
- Lifetime updates and priority support
- Early founder pricing (locked in forever)

If we're late: Every week past March 15 = 20% off, or instant full refund.
100% refund anytime before we ship—just email us.
We'll send launch updates to your email. Unsubscribe anytime.
```

**Output:** Pre-order terms document + microcopy

---

# 🛠️ PLAYBOOK 3: Build & Instrumentation
## Day 3 | Ship the Validation Machine

### **Step 3.1: Technical Build**

**Objective:** Create a fast, accessible, production-ready landing page in hours.

**LLM Prompt:**
```
Output a single responsive HTML file implementing this copy {paste full copy}.

Requirements:
- Semantic HTML5 (header, main, section, footer tags)
- Accessible (ARIA labels, alt text, keyboard navigation)
- FAQ schema as JSON-LD (for SEO rich snippets)
- OpenGraph tags for social sharing
- Inline CSS using utility-first approach (Tailwind-style)
- No external dependencies (no CDN links except Stripe)
- Mobile-first responsive design
- Fast-loading (<2s on 3G)

Include:
- Stripe Payment Link integration for 3 pricing tiers
- Exit survey modal (trigger: 75% scroll or exit intent)
- Event tracking hooks for analytics (commented placeholders)

Design style: {modern/minimalist/bold — specify preference}
```

**What you get:**
- Production-ready HTML file
- Integrated payment flows
- Analytics-ready structure

**Alternative (No-Code):**
If you prefer visual builders:
- **Webflow:** Best for design control
- **Framer:** Great for animations
- **Carrd:** Fastest for simple pages

But single HTML = fastest to iterate.

**Output:** Deployable landing page file

---

### **Step 3.2: Analytics & Instrumentation**

**Objective:** Track every step of the funnel to diagnose conversion leaks.

**Events to Track:**

| Event | When It Fires | What It Tells You |
|-------|---------------|-------------------|
| `view_hero` | Page loads | Traffic volume baseline |
| `cta_primary_click` | Clicks "Pre-order now" | Headline/value prop effectiveness |
| `cta_secondary_click` | Clicks "See demo" | Interest but not ready to commit |
| `form_start` | Begins checkout | Pricing/offer acceptance |
| `form_submit` | Completes form | Friction level acceptable |
| `begin_checkout` | Stripe opens | Real purchase intent |
| `purchase` | Payment success | Actual validation |
| `exit_survey_submit` | Survey completed | Why people didn't buy |

**LLM Prompt:**
```
Create a complete analytics implementation spec for {Plausible/GA4/Mixpanel}:

For each event {list above}, provide:
1. Event name (standardized format)
2. Properties to capture (e.g., source, tier selected, device)
3. JavaScript code snippet (vanilla JS, no jQuery)
4. Placement in HTML (where to add the code)

Also create:
- UTM parameter conventions (source, medium, campaign naming)
- Funnel visualization setup in {analytics tool}
- Dashboard template with key metrics
- Alert conditions (e.g., if purchase rate drops below X%)
```

**Key Metrics Dashboard:**
```
Funnel Overview:
- Traffic → CTA Click: ___% (target: 20-40%)
- CTA Click → Checkout Start: ___% (target: 30-50%)
- Checkout Start → Purchase: ___% (target: 40-70%)
- Overall Conversion Rate: ___% (target: 2-5% for pre-orders)

By Channel:
- Google Search: ___% CVR
- Social: ___% CVR
- Direct: ___% CVR

Exit Survey Themes:
- "Too expensive": ___% 
- "Not clear what it does": ___%
- "Don't need it now": ___%
```

**Output:** Analytics implementation guide + tracking code

---

### **Step 3.3: Exit Survey Setup**

**Objective:** Capture why people don't buy (your most valuable data).

**Survey Questions (3 max):**
```
Trigger: 75% scroll depth OR exit intent

Question 1 (Multi-select + Other):
"What held you back today?"
☐ Price is too high
☐ Not sure if it solves my problem
☐ Don't trust this is real / Need more proof
☐ Need to think about it / Not urgent
☐ Missing a feature I need
☐ Other: [open text]

Question 2 (Range slider):
"What price feels fair for this?"
$0 ——————— $500
[slider with current price marked]

Question 3 (Open text, optional):
"What would we need to add or change for you to buy today?"
[text box]

[Submit] button → "Thanks! Here's 20% off if you change your mind: CODE123"
```

**LLM Prompt:**
```
Create exit survey implementation:
1. HTML/CSS for modal design (non-intrusive, closable)
2. JavaScript trigger logic (scroll depth 75% OR exit intent)
3. Form submission handling (send to {Google Sheets/Airtable/email})
4. Thank you message with incentive code
5. Don't show again logic (cookie, 7 days)

Style: matches landing page design, feels helpful not annoying
```

**Why This Matters:**
If 100 people visit and only 2 buy, you need to know what stopped the other 98. This survey tells you exactly where to improve.

**Output:** Exit survey code + data collection setup

---

### **Step 3.4: Deployment & QA**

**Pre-Launch Checklist:**

**Technical:**
- [ ] Page loads in <2 seconds on mobile
- [ ] All CTAs clickable and tracked
- [ ] Stripe payment flow works (test mode)
- [ ] Exit survey triggers correctly
- [ ] Forms validate properly
- [ ] Mobile responsive (test iPhone + Android)
- [ ] FAQ schema validates (Google Rich Results Test)
- [ ] OpenGraph preview looks good (Facebook Sharing Debugger)

**Copy:**
- [ ] No typos (run through Grammarly)
- [ ] Links work (check every one)
- [ ] Value prop passes "blink test" (show to 3 people for 5 seconds, ask what you sell)
- [ ] Pricing math correct
- [ ] Pre-order terms visible and clear

**Analytics:**
- [ ] All 8 events firing in test
- [ ] UTM parameters working
- [ ] Exit survey submitting to your database

**Deployment:**
- Deploy to **Vercel**, **Netlify**, or **CloudFlare Pages** (free, fast, SSL included)
- Custom domain optional but recommended
- Set up **uptime monitoring** (UptimeRobot free tier)

**Output:** Live landing page URL ready for traffic

---

# PLAYBOOK 4: Traffic & Validation
## Days 4-10 | Get Real Market Feedback

### **Step 4.1: Message Match System**

**Critical Rule:** Your ad copy MUST match your landing page headline exactly (or near-exactly).

**Why:** If your ad says "Save 10 hours/week" but your landing page says "Revolutionary AI Platform"—instant disconnect. User bounces.

**Message Match Framework:**
```
Ad Headline → Landing Page H1 → First Paragraph
(All must reinforce the same promise)

Example:
- Google Ad: "Close deals 3x faster without hiring SDRs"
- Landing H1: "Close deals 3x faster—without hiring SDRs—in 14 days"
- First paragraph: "Stop losing leads to slow follow-ups. Our system closes deals 3x faster..."
```

**LLM Prompt:**
```
For this landing page headline: {H1}

Write 3 ad variants each for:
1. Google Search ads (headline + description + 4 sitelinks)
2. LinkedIn ads (headline + primary text + image suggestion)
3. Meta (Facebook/Instagram) ads (primary text + headline + description)

Requirements:
- Ad headline must exactly mirror or closely paraphrase the landing page H1
- Include 5 keyword themes for Google
- Include 10 negative keywords to avoid wasted spend
- Specify target audience for social ads

Also suggest:
- Landing page URL parameters for tracking (UTM)
- Budget allocation by channel for $500 test budget
```

**Output:** Ad copy library with tracking setup

---

### **Step 4.2: Traffic Strategy (Warm → Cold)**

**Phase 1: Warm Traffic (Days 4-5)**
Target: 200-500 visitors from people who already know/trust you

**Channels:**
1. **Your network:**
   - LinkedIn post (personal profile, not company page)
   - Twitter thread
   - Email to past contacts
   
2. **Relevant communities:**
   - Reddit (if allowed—provide value first, not spam)
   - Slack/Discord communities you're active in
   - Industry forums
   
3. **Ask for feedback:**
   - "I'm validating demand for {product}—would love your honest feedback"
   - Make it feel like exclusive access, not a sales pitch

**Message Match:** Use exact H1 in all posts.

**Phase 2: Cold Traffic (Days 6-10)**
Target: 1,000+ visitors from people who don't know you

**Channel Priority:**

| Channel | Best For | Cost | Speed to Results |
|---------|----------|------|------------------|
| **Google Search** | High-intent buyers | $$$ | 2-3 days |
| **LinkedIn Ads** | B2B, decision-makers | $$$ | 3-5 days |
| **Meta (Facebook/IG)** | B2C, broad reach | $ | 1-2 days |
| **Reddit Ads** | Niche communities | $ | 2-3 days |
| **Twitter Ads** | Tech-savvy audience | $$ | 1-2 days |

**Budget Allocation (Example $500):**
- Google Search: $200 (highest intent)
- LinkedIn OR Meta: $200 (depending on B2B vs B2C)
- Reddit/Twitter: $100 (experimental)

**LLM for Channel Selection:**
```
Based on this product {describe} targeting {ICP}, recommend:
1. Top 3 paid channels with reasoning
2. Budget allocation for $500 test
3. Success metrics for each channel
4. Creative format suggestions (video, carousel, static)
5. Audience targeting parameters
```

---

### **Step 4.3: Daily Analysis & Iteration**

**Objective:** Diagnose conversion leaks and fix them fast.

**Daily Routine (15 minutes):**

1. **Pull funnel data:**
   - Traffic by channel
   - Event conversion rates
   - Purchase count + revenue
   - Exit survey responses (read all of them)

2. **Run LLM analysis:**

**LLM Prompt:**
```
Analyze yesterday's landing page funnel:

Data:
- Traffic: {X} visitors ({Y} from Google, {Z} from LinkedIn, etc.)
- CTA clicks: {N} ({%})
- Checkout started: {N} ({%})
- Purchases: {N} ({%} overall CVR)
- Exit survey top themes:
  * "{Theme 1}": {count}
  * "{Theme 2}": {count}
  * "{Theme 3}": {count}

Questions:
1. Which channel is performing best/worst? Is the difference significant?
2. Where is the biggest drop-off in the funnel?
3. What do exit survey responses tell us?
4. What are the top 3 hypotheses for why people aren't converting?
5. What specific copy, design, or UX changes would address these issues?
6. Should I continue, pivot, or iterate?

Provide:
- Diagnosis of the problem
- Specific fixes ranked by effort vs impact
- Whether to run an A/B test or just update
```

**Conversion Leak Diagnosis:**

| Symptom | Likely Problem | Fix |
|---------|---------------|-----|
| High traffic, low CTA clicks | Headline/value prop unclear | A/B test new H1 |
| High CTA clicks, low checkout starts | Pricing too high or not enough proof | Add guarantee, testimonials, or test lower price |
| High checkout starts, low purchases | Friction in payment flow | Reduce form fields, add payment options |
| Exit survey: "Too expensive" | Pricing perception issue | Show ROI calculator, savings framing, or payment plans |
| Exit survey: "Not clear what it does" | Messaging problem | Rewrite hero section, add demo video |
| Exit survey: "Don't need it now" | Urgency missing | Add scarcity, time-limited offer |

**Output:** Daily action plan with 1-3 high-impact fixes

---

### **Step 4.4: A/B Testing Protocol**

**Objective:** Improve conversion systematically, one variable at a time.

**Testing Priority (do in this order):**

**Test 1: Headline Clarity**
- **Hypothesis:** Outcome-focused headline converts better than clever/vague tagline
- **Variants:**
  - A (control): Current headline
  - B: Pure outcome formula "{Result} in {timeframe}"
- **Metric:** `begin_checkout` rate
- **Sample size:** 200+ visitors per variant
- **Duration:** 2-3 days

**Test 2: Pricing Frame**
- **Hypothesis:** Annual-first with savings callout converts better than monthly-first
- **Variants:**
  - A: Monthly pricing shown first
  - B: Annual pricing shown first with "Save $348/year" badge
- **Metric:** `purchase` count
- **Sample size:** 300+ visitors per variant
- **Duration:** 3-5 days

**Test 3: Social Proof Position**
- **Hypothesis:** Logos/numbers above the fold increase trust and CTA clicks
- **Variants:**
  - A: Social proof below hero
  - B: Social proof in hero section
- **Metric:** `cta_primary_click` rate
- **Sample size:** 200+ visitors per variant
- **Duration:** 2-3 days

**Test 4: Form Friction**
- **Hypothesis:** Email-only vs Email + one qualifier question
- **Variants:**
  - A: Email + "What's your role?" dropdown
  - B: Email only
- **Metric:** `form_submit` rate (watch that `purchase` stays stable)
- **Sample size:** 200+ visitors per variant
- **Duration:** 2-3 days

**Test 5: Guarantee Specificity**
- **Hypothesis:** Date-specific guarantee converts better than generic
- **Variants:**
  - A: "Money-back guarantee"
  - B: "100% refund if we don't ship by March 15, 2025"
- **Metric:** `begin_checkout` rate
- **Sample size:** 200+ visitors per variant
- **Duration:** 2-3 days

**LLM Prompt for Test Design:**
```
Propose 8 A/B tests for this landing page {describe current state}:

For each test, provide:
1. Hypothesis (what you believe and why)
2. Two variants (A = control, B = challenger)
3. Primary metric (what success looks like)
4. Guardrail metrics (what must stay stable)
5. Estimated sample size needed (based on expected effect size)
6. Test duration recommendation
7. Implementation difficulty (easy/medium/hard)

Prioritize by: impact potential / effort required.

# PLAYBOOK 5: Decision Framework
Day 10 | Validate or Pivot
Step 5.1: Define Success Criteria (Before Launch)
Critical: Decide what "success" means BEFORE you get data, or you'll rationalize any result.
Framework Questions:

How many paid pre-orders = green light to build?

Consider: Development cost, time investment, opportunity cost
Example: "20 pre-orders at $49 = $980 revenue = proof of demand"


What conversion rate proves demand?

Pre-order/deposit CVR target: 2-5% is strong
Example: "3% CVR (30 purchases from 1,000 visitors) = validate"


What objections are solvable vs fatal?

Solvable: Price, features, timing, clarity
Fatal: "I don't have this problem" or "This doesn't matter"


How long will you test?

Recommended: 7-10 days with at least 1,000 visitors
Don't judge on day 1 with 50 visitors



LLM Prompt:




# Inspirations

https://www.reddit.com/r/webdesign/comments/1i3go8q/25_best_ui_design_inspiration_websites_for_2025/