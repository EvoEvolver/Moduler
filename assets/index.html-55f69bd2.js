import{_ as a,r as i,o,c as t,a as e,b as n,d,e as l}from"./app-ce233fab.js";const c={},r=l(`<h1 id="moduler" tabindex="-1"><a class="header-anchor" href="#moduler" aria-hidden="true">#</a> Moduler</h1><p>Moduler helps make the skeletons of your Python project more readable by making it <strong>sparse</strong> and <strong>meta-annotated</strong>.</p><p>In Moduler, you can</p><ul><li>Add sections to your functions, classes and modules without refactoring</li><li>Add semantic annotation to your codes. This includes <ul><li>Add examples to your existing codes</li><li>Add todos for incomplete codes</li></ul></li></ul><p>We believe in this way we can provide much more context information to new contributors who are not familiar with the codebase. It is also important for AI-based agents to understand the codebase and develop it.</p><h2 id="how-to-use" tabindex="-1"><a class="header-anchor" href="#how-to-use" aria-hidden="true">#</a> How to use</h2><h3 id="sections" tabindex="-1"><a class="header-anchor" href="#sections" aria-hidden="true">#</a> Sections</h3><p>Putting sections in Moduler is as easy as putting sections in Markdown. You just need to put a <code>#</code> before your section title in a comment environment starting with <code>&quot;&quot;&quot;</code>. For example,</p><div class="language-python line-numbers-mode" data-ext="py"><pre class="language-python"><code><span class="token triple-quoted-string string">&quot;&quot;&quot;
# Section 1
The following is a function.
&quot;&quot;&quot;</span>


<span class="token keyword">def</span> <span class="token function">foo</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">pass</span>


<span class="token triple-quoted-string string">&quot;&quot;&quot;
# Section 2
The following is another function.
&quot;&quot;&quot;</span>


<span class="token keyword">def</span> <span class="token function">bar</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">pass</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>In this way, <code>foo()</code> and <code>bar()</code> will have sections <code>Section 1</code> and <code>Section 2</code> respectively. The sections will also contain the comments under them.</p><p>Your section can also contain classes add levels. For example,</p><div class="language-python line-numbers-mode" data-ext="py"><pre class="language-python"><code><span class="token triple-quoted-string string">&quot;&quot;&quot;
# Top Section
## Section 1
&quot;&quot;&quot;</span>


<span class="token keyword">class</span> <span class="token class-name">Foo</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">&quot;&quot;&quot;
    # Section 1
    The following is a function.
    &quot;&quot;&quot;</span>

    <span class="token keyword">def</span> <span class="token function">foo</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">pass</span>

    <span class="token triple-quoted-string string">&quot;&quot;&quot;
    # Section 2
    The following is another function.
    &quot;&quot;&quot;</span>

    <span class="token keyword">def</span> <span class="token function">bar</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">pass</span>


<span class="token triple-quoted-string string">&quot;&quot;&quot;
## Section 2
&quot;&quot;&quot;</span>


<span class="token keyword">def</span> <span class="token function">baz</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">pass</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="section-in-folder" tabindex="-1"><a class="header-anchor" href="#section-in-folder" aria-hidden="true">#</a> Section in folder</h3><p>You add <code>.tree.yml</code> file in a folder to add sections in it. For example, in the following folder</p><div class="language-text line-numbers-mode" data-ext="text"><pre class="language-text"><code>a_folder
- __init__.py
- a.py
- b.py
- c.py
- .tree.yml
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>You can put <code>a</code>,<code>b</code> in a section by putting</p><div class="language-yaml line-numbers-mode" data-ext="yml"><pre class="language-yaml"><code><span class="token key atrule">sections</span><span class="token punctuation">:</span>
 <span class="token key atrule">your section title</span><span class="token punctuation">:</span>
   <span class="token punctuation">-</span> a
   <span class="token punctuation">-</span> b
<span class="token key atrule">default section</span><span class="token punctuation">:</span> you default section title
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>Then <code>a</code> and <code>b</code> will be in the section <code>your section title</code> and <code>c</code> will be in the section <code>you default section title</code>.</p><h3 id="mark-examples" tabindex="-1"><a class="header-anchor" href="#mark-examples" aria-hidden="true">#</a> Mark examples</h3><p>You can also add examples to your functions and classes. Just use the <code>@example</code> decorator. For example,</p><div class="language-python line-numbers-mode" data-ext="py"><pre class="language-python"><code><span class="token keyword">from</span> moduler<span class="token punctuation">.</span>decorator <span class="token keyword">import</span> example


<span class="token decorator annotation punctuation">@example</span>
<span class="token keyword">def</span> <span class="token function">how_to_use_foo</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">&quot;&quot;&quot;
    The following is an example of using \`foo()\`.
    &quot;&quot;&quot;</span>
    foo<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="mark-todos" tabindex="-1"><a class="header-anchor" href="#mark-todos" aria-hidden="true">#</a> Mark todos</h3><p>In a similar way, you can also mark todos in your code. Just use the <code>@todo</code> decorator. For example,</p><div class="language-python line-numbers-mode" data-ext="py"><pre class="language-python"><code><span class="token keyword">from</span> moduler<span class="token punctuation">.</span>decorator <span class="token keyword">import</span> todo


<span class="token decorator annotation punctuation">@todo</span>
<span class="token keyword">def</span> <span class="token function">todo_foo</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">&quot;&quot;&quot;
    The following is a todo.
    &quot;&quot;&quot;</span>
    foo<span class="token punctuation">(</span><span class="token punctuation">)</span>


<span class="token decorator annotation punctuation">@todo</span><span class="token punctuation">(</span><span class="token string">&quot;This function is buggy. Fix it.&quot;</span><span class="token punctuation">)</span>
<span class="token keyword">def</span> <span class="token function">buggy_foo</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    foo<span class="token punctuation">(</span>a<span class="token operator">=</span>b<span class="token punctuation">)</span>
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="visualize-your-codebase" tabindex="-1"><a class="header-anchor" href="#visualize-your-codebase" aria-hidden="true">#</a> Visualize your codebase</h2><p>You can put the function <code>draw_module_tree()</code> in any of your modules to visualize the tree structure generated from it. Call it in the <code>__init__.py</code> of your package is recommended.</p><h2 id="installation" tabindex="-1"><a class="header-anchor" href="#installation" aria-hidden="true">#</a> Installation</h2><p>You can install Moduler by</p><div class="language-bash line-numbers-mode" data-ext="sh"><pre class="language-bash"><code>pip <span class="token function">install</span> git+https://github.com/EvoEvolver/Moduler.git
</code></pre><div class="line-numbers" aria-hidden="true"><div class="line-number"></div></div></div><h2 id="philosophy-behind-moduler" tabindex="-1"><a class="header-anchor" href="#philosophy-behind-moduler" aria-hidden="true">#</a> Philosophy behind Moduler</h2><h3 id="sparse-tree-structure" tabindex="-1"><a class="header-anchor" href="#sparse-tree-structure" aria-hidden="true">#</a> Sparse tree structure</h3><p>All the programming languages encourage the programmers to put their code in the tree structure. For example, you can put your functions in difference classes, in different files and put the files in different folders. However, it is still very common to put a lot of functions in a single file, in which the codes are arranged in an almost flat structure.</p><p>Moduler helps this by adding a zero-cost way to add sections to your functions and classes. It makes another step towards a more tree-like structure of the codebase. We believe this will help the programmers to understand the codebase better.</p><h3 id="literate-programming" tabindex="-1"><a class="header-anchor" href="#literate-programming" aria-hidden="true">#</a> Literate programming</h3>`,34),u={href:"https://guides.nyu.edu/datascience/literate-prog",target:"_blank",rel:"noopener noreferrer"};function p(v,m){const s=i("ExternalLinkIcon");return o(),t("div",null,[r,e("p",null,[n("Moduler can be regarded as an effort toward the idea - "),e("a",u,[n("literate programming"),d(s)]),n(". We think literate programming gets even more important in the era of AI for it provides more context information for AI-based agents to understand the codebase.")])])}const b=a(c,[["render",p],["__file","index.html.vue"]]);export{b as default};
