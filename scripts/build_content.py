"""Build editorial HTML and exact SVG infographic sources using only stdlib.
PNG exports are committed; regenerate with scripts/render_diagrams.sh.
"""
import json, html, textwrap
from pathlib import Path
R=Path(__file__).resolve().parent.parent
A=json.loads((R/'content/articles.json').read_text())
BASE='https://syntriq-org.github.io/site/'
e=html.escape

def nav(prefix=''):
 return '<a class="skip" href="#main">Skip to content</a><header id="header"><div class="nav-wrap"><a class="brand" href="'+prefix+'index.html" aria-label="Syntriq home"><span class="brand-image" role="img" aria-label="Syntriq"></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span>☰</span></button><nav id="navigation" aria-label="Main navigation">'+''.join(f'<a href="{prefix}{url}">{label}</a>' for url,label in [('platform.html','Platform'),('ai-studio.html','AI & Studio'),('applications.html','Applications'),('insights/index.html','Insights'),('architecture.html','Architecture')])+'</nav></div></header>'
def page(title,desc,path,body,prefix='',img='assets/hero.webp'):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} — Syntriq</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#090f1a"><link rel="canonical" href="{BASE+path}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{'article' if path.startswith('insights/') and path!='insights/index.html' else 'website'}"><meta property="og:url" content="{BASE+path}"><meta property="og:image" content="{BASE+img}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}app.js" defer></script></head><body>{nav(prefix)}<main id="main">{body}</main><footer><div class="container footer-inner"><a class="brand" href="{prefix}index.html" aria-label="Syntriq home"><span class="brand-image" role="img" aria-label="Syntriq"></span></a><span>Connected data. Coordinated processes.</span><small>© <span id="year">2026</span> Syntriq</small></div></footer></body></html>'''
def card(a,prefix=''):
 art={'one-connected-business-story':'connected-business','ai-with-application-context':'ai-context','simulate-before-you-release':'simulation-evidence'}
 if a['slug'] in art:
  src=f"assets/insights/{art[a['slug']]}.png"; w,h=1536,1024
 else:
  src=f"assets/diagrams/{a['slug']}-preview.png"; w,h=1000,650
 return f'<a class="insight-card" href="{prefix}insights/{a["slug"]}.html"><img src="{prefix}{src}" alt="{e(a["deck"])}" width="{w}" height="{h}" loading="lazy"><div class="insight-card-copy"><span class="eyebrow">{e(a["category"])}</span><h3>{e(a["title"])}</h3><p>{e(a["deck"])}</p><span class="text-link">Read the story ↗</span></div></a>'
def figure(a,prefix=''):
 name=a['slug'];alt='; '.join(n[0]+': '+n[1] for n in a['nodes'])
 return f'<figure class="container article-figure"><img src="{prefix}assets/diagrams/{name}.png" srcset="{prefix}assets/diagrams/{name}-preview.png 1000w, {prefix}assets/diagrams/{name}.png 2000w" sizes="(max-width: 1200px) 100vw, 1200px" alt="{e(alt)}" width="2000" height="1300" loading="lazy"><figcaption><span>How the capabilities connect</span></figcaption></figure>'
def rich_figure(a):
 art={
  'one-connected-business-story':('connected-business','A shared application model connects business entities, workflows, analytics and AI-assisted engineering.'),
  'ai-with-application-context':('ai-context','A browser workbench connects an application catalogue, cloud reasoning, engineering tools and a visible evidence journal.'),
  'simulate-before-you-release':('simulation-evidence','Routine, boundary and fault scenarios feed a simulation laboratory, evidence collection and a verification gateway.')
 }
 if a['slug'] not in art: return ''
 name,alt=art[a['slug']]; src='../assets/insights/'+name+'.png'
 return f'<figure class="container article-figure rich-infographic"><img src="{src}" alt="{e(alt)}" width="1536" height="1024" loading="lazy"><figcaption><span>{e(alt)}</span></figcaption></figure>'
def svg(a):
 s=['<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1300" viewBox="0 0 2000 1300"><defs><radialGradient id="bg"><stop stop-color="#133744"/><stop offset="1" stop-color="#090f1a"/></radialGradient><linearGradient id="card" x2="1" y2="1"><stop stop-color="#183844"/><stop offset="1" stop-color="#0e1a2a"/></linearGradient><linearGradient id="accent"><stop stop-color="#20bbae"/><stop offset="1" stop-color="#31c3ea"/></linearGradient><marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#31c3ea" stroke-width="1.4"/></marker></defs><rect width="2000" height="1300" fill="url(#bg)"/>']
 for x in range(60,2000,60):
  for y in range(50,1300,60): s.append(f'<circle cx="{x}" cy="{y}" r="1" fill="#447788" opacity=".22"/>')
 def txt(x,y,t,size=28,color='#c1d3df',weight=400):s.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{weight}">{e(t)}</text>')
 txt(100,88,'SYNTRIQ  /  '+a['category'].upper(),23,'#43d8c9',600)
 for i,line in enumerate(textwrap.wrap(a['title'],46)):txt(100,178+i*66,line,54,'#f1f8fb',600)
 txt(100,320,'Connected definitions. Visible behaviour. Inspectable evidence.',26)
 # serpentine six-stage layout, three columns, generous open space
 coords=[(100,390),(730,390),(1360,390),(1360,790),(730,790),(100,790)]
 edges=['M650 540 H710','M1280 540 H1340','M1635 690 V768','M1360 940 H1300','M730 940 H670']
 for d in edges:s.append(f'<path d="{d}" fill="none" stroke="#31c3ea" stroke-width="3" marker-end="url(#arrow)"/>')
 for i,((x,y),(title,sub)) in enumerate(zip(coords,a['nodes'])):
  s.append(f'<rect x="{x+8}" y="{y+12}" width="550" height="300" rx="24" fill="#030811" opacity=".5"/><rect x="{x}" y="{y}" width="550" height="300" rx="24" fill="url(#card)" stroke="#3b6878" stroke-width="2"/><rect x="{x+32}" y="{y+32}" width="64" height="64" rx="16" fill="#123f46" stroke="#20bbae"/>')
  txt(x+45,y+76,f'{i+1:02}',28,'#63eee0',600)
  for j,line in enumerate(textwrap.wrap(title,24)):txt(x+32,y+150+j*40,line,34,'#f1f8fb',600)
  for j,line in enumerate(textwrap.wrap(sub.replace(' · ',' / '),33)):txt(x+32,y+237+j*32,line,25)
 if a['slug'] in ('ai-with-application-context','engineering-request-to-evidence','simulate-before-you-release'):
  s.append('<path d="M100 940 H55 V540 H78" fill="none" stroke="#20bbae" stroke-width="3" stroke-dasharray="9 9" marker-end="url(#arrow)"/>')
  txt(100,1150,'FEEDBACK / Return findings to the next bounded engineering step',25,'#43d8c9')
 else:txt(100,1150,'READ AS A CONNECTED MODEL / Each layer retains its own responsibility',23,'#43d8c9')
 s.append('<path d="M100 1190 H1900" stroke="#355463"/>');txt(100,1245,'SYNTRIQ',24,'#f1f8fb',600);txt(350,1245,'Connected data. Coordinated processes.',22)
 s.append('</svg>');return ''.join(s)
for i,a in enumerate(A):
 (R/'assets/diagrams'/f'{a["slug"]}.svg').write_text(svg(a))
 toc='<nav class="article-toc" aria-label="Article sections">'+''.join(f'<a href="#section-{j}">{e(h)}</a>' for j,(h,_) in enumerate(a['sections']))+'</nav>'
 reading='<article class="article-content"><div class="article-body article-segment">'+toc+'</div>'
 for j,(h,t) in enumerate(a['sections']):
  reading+=f'<section class="article-body article-segment" id="section-{j}"><h2>{e(h)}</h2>'+''.join('<p>'+e(p)+'</p>' for p in t.split('\n'))+'</section>'
  if j == 0: reading+=rich_figure(a)
  if j == 2: reading+=figure(a,'../')
 reading+='<div class="article-body"><div class="takeaway"><span>THE BUSINESS VALUE</span><p>'+e(a['takeaway'])+'</p></div></div></article>'
 body=f'<div class="container article-heading"><a class="back-link" href="index.html">← All insights</a><div class="eyebrow">SYNTRIQ INSIGHTS / {e(a["category"])}</div><h1>{e(a["title"])}</h1><p class="article-deck">{e(a["deck"])}</p></div>'+reading+'<section class="container related"><div class="eyebrow">CONTINUE EXPLORING</div><h2>Follow the connected story.</h2><div class="insights-grid two">'+card(A[(i+1)%len(A)],'../')+card(A[(i+3)%len(A)],'../')+'</div></section>'
 (R/'insights'/f'{a["slug"]}.html').write_text(page(a['title'],a['deck'],f'insights/{a["slug"]}.html',body,'../',f'assets/diagrams/{a["slug"]}.png'))
body='<div class="container article-heading"><div class="eyebrow">SYNTRIQ INSIGHTS</div><h1>The thinking behind<br>the connected platform.</h1><p class="article-deck">Explore business meaning, explainable decisions and AI-assisted engineering. Start with the overview, then follow the connections that matter to you.</p><div class="topic-links"><a href="#foundation">Platform foundations</a><a href="#engineering">AI & engineering</a><a href="#domain">Applications</a></div></div>'
for id,title,indices in [('foundation','Understand the platform',[0,3,4,5,6,7]),('engineering','Build with context and evidence',[1,2,8]),('domain','See the application boundary',[9])]:
 body+=f'<section class="container insights-list" id="{id}"><h2>{title}</h2><div class="insights-grid">'+''.join(card(A[i],'../') for i in indices)+'</div></section>'
(R/'insights/index.html').write_text(page('Insights','Visual explanations of the Syntriq platform, AI integration and application architecture.','insights/index.html',body,'../'))
hubs=[
('platform','Platform','Business meaning, carried through your application.','Connect models, constraints, decisions, processes, history and analytics through explicit contracts.',0,[3,4,5,6,7], [('A foundation with clear responsibilities','The ontology defines business meaning. Constraints validate facts. Policies evaluate decisions. Workflows coordinate tasks, and commands apply permitted changes. Temporal and analytical contracts preserve the context needed to interpret outcomes.'),('Typed access to a connected model','GraphQL exposes supported data and metadata through typed interfaces. It gives consumers access to the model while retaining ontology identity, relevant constraints and time perspectives.'),('One example, many connected views','An agreement moves from a form to a policy decision, a review task and an analytical measure. Shared definitions connect these views so a change can be investigated across the application.')]),
('ai-studio','AI & Studio','Give AI a working understanding of your application.','A browser-first workbench connects application context, cloud reasoning and executable evidence.',1,[8,2,4],[('Discover before proposing','The application catalogue connects sources and dependencies. The Context Engine selects relevant definitions for a bounded task. Source versions and unresolved questions remain visible to the engineer.'),('Reason through an authenticated connection','The integration architecture uses an OpenAI Responses adapter through an authenticated relay. The browser coordinator owns the task, and the capability broker validates supported tool requests. Model credentials are never part of this public static site.'),('Inspect the candidate and its evidence','Candidate changes are isolated and compared with their baseline. Local runtime tools return checks and traces. A task journal records attempts, while optional external providers contribute explicitly configured capabilities.'),('Follow an illustrative engineering journey','Ask for an additional approval condition, inspect its dependencies, propose a candidate and exercise boundary scenarios. This page explains the integration architecture; it does not send prompts to a live model.')]),
('applications','Applications','A shared platform. A domain that stays yours.','ChargeWeave shows how industry definitions connect to a reusable application foundation.',9,[9,7,5],[('ChargeWeave supplies the EV application','Its domain package defines charging entities, relationships, policies, workflows, measures and presentation. Settlement and correction journeys provide concrete examples of connected behaviour.'),('Syntriq supplies the mechanisms','The reusable layer handles supported queries, constraints, decisions, process coordination and engineering tools through explicit contracts. The core should not acquire hidden charging-specific branches.'),('Preserve behaviour as the boundary evolves','Technical development can continue inside ChargeWeave. Reference journeys and contract checks provide the basis for extracting reusable mechanisms into Syntriq without replacing domain definitions.')]),
('architecture','Architecture','Clear contracts between connected capabilities.','A practical guide to the responsibilities behind the product story.',0,[3,4,6,7,8],[('Meaning and access','RDF/OWL identities and SHACL constraints form part of the semantic foundation through a declared supported subset. GraphQL exposes supported data and metadata; it does not replace the semantic model.'),('Evaluation and execution','A versioned decision evaluator returns outcomes, calculations, reasons and missing information. XFlow/XState coordinate processes and states. Commands enforce permitted changes and declared duplicate behaviour.'),('Time and analysis','Effective time and recorded knowledge establish the perspective of facts. Measures declare grain, units, aggregation behaviour, filters, completeness and knowledge cutoff so consumers can interpret results.'),('AI engineering boundary','Catalogue discovery, context selection, candidate isolation, task journaling and capability dispatch belong to the workbench architecture. An authenticated relay connects reasoning providers; tools return evidence tied to candidate and source versions.'),('Browser workbench and service boundaries','Local simulation and engineering tools can run beside the preview without requiring a complete business backend. The authenticated AI relay is a separate service boundary. Business persistence, shared execution and backend deployment require their own contracts.'),('Connected responsibilities','Explicit contracts connect application definitions, runtime behaviour and engineering evidence. Each capability retains a clear responsibility while sharing the context needed to work with the others.')])]
for slug,label,title,deck,visual,indices,sections in hubs:
 body=f'<div class="container article-heading"><div class="eyebrow">SYNTRIQ / {e(label)}</div><h1>{e(title)}</h1><p class="article-deck">{e(deck)}</p></div>'+figure(A[visual])+ '<div class="article-body">'+''.join(f'<section><h2>{e(h)}</h2><p>{e(t)}</p></section>' for h,t in sections)+'</div><section class="container related"><h2>Explore the details.</h2><div class="insights-grid">'+''.join(card(A[i]) for i in indices)+'</div></section>'
 (R/f'{slug}.html').write_text(page(label,deck,slug+'.html',body,img=f'assets/diagrams/{A[visual]["slug"]}.png'))
# Update the retained visual homepage rather than replace its original artwork.
p=R/'index.html';s=p.read_text();start=s.index('<a class="skip"');end=s.index('<main id="main">');s=s[:start]+nav()+s[end:]
s=s.replace('a GraphQL-first data engine, visual process orchestration and an integrated Studio','an ontology-driven application platform with explainable decisions, coordinated processes and contextual AI')
s=s.replace('GraphQL-first','Ontology-driven').replace('Express entities, relationships and business structure through a GraphQL-first data engine. Query your model through the same language that defines it.','Define entities, relationships and business meaning through an ontology-driven model. Access supported data and metadata through typed GraphQL interfaces.')
s=s.replace('Express entities, relationships and business structure through a Ontology-driven data engine. Query your model through the same language that defines it.','Define entities, relationships and business meaning through an ontology-driven model. Access supported data and metadata through typed GraphQL interfaces.')
s=s.replace('Native GraphQL','Typed GraphQL').replace('Design business flows visually with BPMN. Connect data changes to process execution and make the path from event to action explicit.','Connect events, business decisions and tasks through explicit process contracts. Make the path from a fact to a permitted action inspectable.').replace('BPMN modeling','Process contracts')
s=s.replace('Move between schemas, queries, tables and process models in an integrated Studio. Explore the system without losing its context.','Connect application definitions, selected context and engineering tools in a browser-first workspace. Examine candidate changes through visible evidence.')
s=s.replace('Visual workspace','Contextual AI').replace('Query tools','Scenario evidence')
s=s.replace('Bring the structure of your business and the flow of your work closer together. Meet Syntriq.','Connect business models, rules, processes and insights—with AI that works from the context of your application.')
s=s.replace('href="#platform">Discover the platform','href="platform.html">Discover the platform')
s=s.replace('href="#studio">Inside Syntriq Studio','href="ai-studio.html">Inside Syntriq Studio')
s=s.replace('<span>GraphQL-first</span>','<span>Ontology-driven</span>')
s=s.replace('<meta name="theme-color"',f'<link rel="canonical" href="{BASE}"><meta name="twitter:card" content="summary_large_image"><meta property="og:url" content="{BASE}"><meta name="theme-color"',1) if 'rel="canonical"' not in s else s
start=s.index('<section class="section container" id="insights">');end=s.index('<section class="section container explore-section',start)
s=s[:start]+'<section class="section container" id="insights"><div class="split-heading"><div><div class="eyebrow">05 / INSIGHTS</div><h2>Explore the connected platform.</h2></div><a class="text-link" href="insights/index.html">All ten visual guides ↗</a></div><div class="insights-grid">'+''.join(card(A[i]) for i in [0,1,8])+'</div></section>'+s[end:]
p.write_text(s)
# Canonical sitemap includes only public HTML pages.
paths=['index.html','platform.html','ai-studio.html','applications.html','architecture.html','insights/index.html']+['insights/'+a['slug']+'.html' for a in A]
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+('' if p=='index.html' else p)+'</loc></url>' for p in paths)+'</urlset>')
print('Built',len(paths),'pages and',len(A),'SVG sources.')
