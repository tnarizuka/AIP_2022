#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys, os
import numpy as np
import matplotlib.pyplot as plt
try:
    import japanize_matplotlib
except:
    pass
import pandas as pd
pd.set_option('display.precision', 3)   # 小数点以下の表示桁
pd.set_option('display.max_rows', 20)  # 表示する行数
get_ipython().run_line_magic('precision', '3')


# # 特性値の活用

# ## データの中心を表す特性値

# ### 算術平均

# データの中心を表す特性値として最もよく知られ，よく用いられるのが**算術平均**であり，
# 
# $$
# 	\bar{x} = \frac{x_{1}+x_{2}+\cdots+x_{n}}{n} = \frac{1}{n} \sum_{i=1}^{n}x_{i}
# $$(eq:arithmetic_mean)
# 
# と定義される．
# ただし，算術平均は分布形状が左右対称に近いデータの場合にはデータの中心を表す量と捉えられるが，分布形状が極端に非対称な場合にはデータの中心を表す特性値としてふさわしくない．

# 算術平均は度数分布表から求めることもできる．
# 具体的には，階級値を$ v_{i} $，対応する度数を$ f_{i} $，階級の数を$ k $とすると，平均値は
# 
# $$
# 	\bar{x} = \frac{f_{1}v_{1}+f_{2}v_{2}+\cdots+f_{k}v_{k}}{f_{1}+f_{2}+\cdots+f_{k}}
# 	= \frac{1}{n} \sum_{i=1}^{k} f_{i}v_{i}
# $$(eq:arithmetic_mean2)
# 
# と表される．

# 以上をPythonで実装してみよう．
# まずはアヤメデータを読み込む．

# In[5]:


# アヤメデータの読み込み
Iris = pd.read_csv('Iris.csv')
Iris = Iris.iloc[:, 1:5]
Iris.columns=['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']


# このデータに対し，式{eq}`eq:arithmetic_mean`を当てはめれば算術平均を計算することができる．
# 例えば，アヤメのがく片の長さのデータの場合，平均値は$ \bar{x}=5.843 $ cmとなる．

# In[11]:


# アヤメのがく片の長さの平均
Iris['Sepal Length'].mean()


# 一方，がく片の長さに対する度数分布表は以下のようになる．

# In[8]:


# ビンの個数（スタージェスの公式）
bn = int(1+np.log2(len(Iris)))

# がく片の長さに対する度数分布表
f, x = np.histogram(Iris['Sepal Length'], bins=bn, density=0)
df = pd.DataFrame(np.c_[x[:-1], x[1:], 0.5*(x[1:]+x[:-1]), f, 100*f/len(Iris), 100*np.cumsum(f/len(Iris))],
                  columns=['最小', '最大', '階級値', '度数', '相対度数', '累積相対度数'])
df


# この度数分布表のデータを式{eq}`eq:arithmetic_mean2`に当てはめれば算術平均を計算することができる．
# 実際にアヤメのがく片に対して算術平均を求めると，$ \bar{x}=5.854 $ cmとなる．

# In[12]:


# アヤメのがく片の長さの平均（度数分布表から求めたもの）
np.sum(df['度数']*df['階級値'])/np.sum(df['度数'])


# 以上の例を見て分かるように，度数分布表から求めた平均値はデータから直接求めた平均値と一致しない．
# これは，度数分布表から求めた平均値が近似値であるからである．
# 度数分布表では，各階級の値を階級値で代表させているためこのようなことが起こるが，各階級の幅を十分小さく取れば近似の度合いは上昇する．

# ### 幾何平均

# 算術平均に対して，幾何平均というものも存在する．
# これは，$ n $個のデータに対して，値の積の$ n $乗根をとったもので，
# 
# $$
# 	\bar{x}_{g} = \sqrt[n]{x_{1}\times\cdots \times x_{n}} = \sqrt[n]{\prod_{i=1}^{n}x_{i}} = \left(\prod_{i=1}^{n}x_{i}\right)^{1/n}
# $$(eq:geometric_mean)
# 
# と定義される．
# 定義より，幾何平均は正の数のみしか扱えず，さらに掛け算によって定義されるので比率データにしか適用できない．
# 
# 幾何平均は成長率や倍率の平均を計算するときに用いられる．
# 例えば，次のような事例を考える：
# ```
# 1年目から2年目にかけての物価は対前年比2倍になり（100円のものが200円になり），2年目から3年目にかけての物価は対前年比8倍となった（200円のものが1600円になった）．
# では，この2年間の物価の対前年比伸び率の平均はいくらか？
# ```
# まず，算術平均を適用してみる．
# すると，物価の対前年比伸び率の平均は$ (2+8)/2=5 $倍となる．
# これは，1年目に100円だったものが2年目に500円になり，さらに3年目に2500円になることを意味するので，実際よりも過大に見積もってしまう．
# そこで，次に幾何平均を適用してみる．
# すると，物価の対前年比伸び率の平均は$ \sqrt[2]{2\times 8}=4 $倍となる．
# これは，1年目に100円だったものが2年目に400円になり，さらに3年目に1600円になることを意味するので，実際の金額と一致する．
# このように，倍率の平均値を計算する場合には，算術平均ではなく幾何平均を用いるのが妥当である．

# **Pythonによる実装**

# In[11]:


from scipy.stats.mstats import gmean


# In[12]:


gmean(Iris['Sepal Length'])


# ### 中央値

# データの分布形状が歪んでいる場合，算術平均はデータの中心を表す特性値としてふさわしくない．
# 例えば，
# 
# $$
# 	1,1,1,1,2,3,4,5,16,20 
# $$
# 
# のようなデータがあったとき，この算術平均は5.4になるが，平均より小さいものが8個を占め，残りの2個が平均より大きい．
# これは，少数のデータ（16と20）が平均を押し上げている例である．
# このような場合，分布の中心という意味では既に述べた**中央値（メディアン）**を用いる方が適切である．
# 実際，中央値を用いれば，その値より小さい数と大きい数の個数が等しくなる．

# **Pythonによる実装**

# In[13]:


Iris['Sepal Length'].median()


# ### 最頻値

# 平均値，中央値の他によく用いられる特性値として，**最頻値**（モード）がある．
# これは，データの中で最も頻出する数であり，度数分布表において度数が最大となる階級の階級値に対応する．
# ただし，分布形状が双峰性の場合には有効な特性値とならないので注意が必要である．

# **Pythonによる実装**

# In[14]:


Iris['Sepal Length'].mode()


# ## データのばらつきを表す特性値

# データの特性を知りたい場合，中心を表す特性値だけでは情報不足であり，中心からどの程度ばらついているかも考慮しなければならない．
# 例えば，以下の3つのデータは中心を表す算術平均，中央値，最頻値がすべて5であるが，分布の形状は異なる．
# 
# \begin{align*}
# 	&A: 0,3,3,5,5,5,5,7,7,10 \\
# 	&B: 0,1,2,3,5,5,7,8,9,10 \\
# 	&C: 3,4,4,5,5,5,5,6,6,7
# \end{align*}

# 通常，ばらつきを求める際には，算術平均からの距離$ x_{i} - \bar{x} $を考える．
# これを**偏差**と呼ぶ．
# この偏差を全データに対して平均すれば，ばらつきを表す特性値になりそうであるが，これだと問題が生じる．
# 例えば，データが左右対称に分布している場合，平均より小さい値のデータ（偏差が負）と大きい値のデータ（偏差が正）が同程度あるため，偏差を平均するとほぼ0になってしまう．
# ばらつきが0というのは明らかにおかしいため，別の特性値を考える必要がある．
# 以下に代表的な方法を示す．

# ### 平均偏差

# １つ目の方法は偏差の絶対値を取ってから平均するというものであり，**平均偏差**と呼ばれる：
# 
# $$
# 	平均偏差 = \frac{1}{n} \sum_{i=1}^{n}|x_{i}-\bar{x}| 
# $$(eq:mean_deviation)
# 
# 
# これは，$ n $個のデータの1個当りの平均からの距離であり，ばらつきの指標として直感的に理解しやすい．
# しかし，絶対値の扱いが数学的に面倒，分布の中心が$ \bar{x} $ではなく中央値のときに最小になる，平均から大きく外れた値も等しい寄与となる，など問題があるため利用されることは少ない．

# **Pythonによる実装**

# In[ ]:


np.fabs(Iris['Sepal Length'] - Iris['Sepal Length'].mean()).mean()


# ### 分散・標準偏差

# ２つ目の方法は，偏差の２乗をとってから平均するというものであり，**分散**と呼ばれる：
# 
# $$
# 	s^{2} = \frac{1}{n} \sum_{i=1}^{n} (x_{i} - \bar{x})^{2}
# $$(eq:deviation)
# 
# 分散は$ n $個のデータ1個当りの平均からの距離の2乗であり，平均から大きく離れるほど寄与が大きくなる指標である．
# %特に，平均偏差と対照的に，分布の中心が$ \bar{x} $のときに最小となる．
# 
# 
# また，分散の平方根$ s $は**標準偏差**と呼ばれる：
# 
# $$
# 	s = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_{i} - \bar{x})^{2}}
# $$(eq:standard_deviation)
# 
# 標準偏差はデータの測定単位と同一の単位となるので扱いやすい．
# 通常，データのばらつきを表す特性値としては分散または標準偏差が最もよく用いられる．

# **Pythonによる実装**

# In[ ]:


# 分散
Iris['Sepal Length'].var()


# In[ ]:


# 標準偏差
Iris['Sepal Length'].std()


# ### 変動係数

# 標準偏差は測定単位によって値が変化してしまう．
# また，データの水準の変化（おおまかには平均値の大きさ）とともに標準偏差の大きさは変化する．
# そこで，データの水準を平均値によって調整した指標が**変動係数**（Coefficient of Variation）で，次式で定義される：
# 
# $$
# 	\mathrm{CV} = \frac{s}{\bar{x}}
# $$(eq:cv)
# 
# 変動係数は同じ単位を持つ量同士で割り算をしているので，無次元（単位がない）となり，データの測定単位に寄らない．
# 通常，単位や平均が異なるグループ間でばらつきを比較する際には変動係数が用いられる．

# **Pythonによる実装**

# In[ ]:


Iris['Sepal Length'].std()/Iris['Sepal Length'].mean()


# ## ローレンツ曲線とジニ係数

# ある社会を構成する構成員（人物でも市町村でも何でも良い）に対し，所得が対応したデータを考える．
# この構成員を所得の小さい順に並べて$ n $個の階級に分け，階級$ i $のサイズ（人数や個数）を$ x_{i} $，平均所得を$ y_{i} $とする．
# また，サイズの累積相対度数を$ X_{i} $，平均所得の累積相対度数を$ Y_{i} $とする．
# このとき，横軸に構成員の累積相対度数，縦軸に所得の累積相対度数を取ったグラフを**ローレンツ曲線**と呼ぶ．
# グラフの横軸，縦軸はともに0から1の範囲であり，曲線上の$ (X, Y) $という点は，社会全体の貧しい側から$ X\times100 $\%の人が全体の$ Y\times100 $\%の富を占めることを表す．
# 例えば，$ (0.25, 0.1) $という点は，社会全体の25\%の人が10\%の富を占めるということを表す．
# ローレンツ曲線はこれらの点を点線で結んだ折れ線グラフとして表され，必ず両端が$ (0, 0) $と$ (1, 1) $になる．
# もし，富が全構成員に平等に配分されている場合，ローレンツ曲線は傾き1の直線となり，これを**完全平等線**と呼ぶ．
# 一方，富の配分に格差があるほどローレンツ曲線は完全平等線から下にずれていく．
# このように，ローレンツ曲線はある社会における富の配分格差を可視化したグラフといえる．
# 
# 社会の格差の度合いはローレンツ曲線が完全平等線から下にずれるほど大きくなる．
# よって，ローレンツ曲線と完全平等線によって囲まれた部分の面積が，完全平等線，$ x=1 $，$ y=0 $で構成される三角形の面積に占める割合を格差の指標と考えることができる．
# この指標は**ジニ係数**と呼ばれる．
# 階級を$ n $等分したとき，下から$ i $番目の階級の平均所得を$ y_{i} $とする（$ y_{1}\leq y_{2} \leq \cdots \leq y_{n} $）．
# このとき，ジニ係数を以下のように表すこともできる：
# 
# $$
# 	G = \frac{1}{2n^{2} \bar{y}} \sum_{i=1}^{n} \sum_{j=1}^{n} |y_{i} - y_{j}|
# $$(eq:gini)
# 
# ただし，$ \bar{y} = \frac{1}{n} \sum_{i=1}^{n} y_{i} $は全体の平均所得である．
# ジニ係数は0から1の間で定義され，完全に平等な配分のときに$ G=0 $，一人がすべての所得を占有しているときに$ G=(n-1)/n $となる（つまり$ n $が大きいときには1に近づく）．

# **例）$ n=3 $の場合**
# 
# まず，式{eq}`eq:gini`を用いてジニ係数を計算すると，
# \begin{align*}
# 	\sum_{i=1}^{3}\sum_{j=1}^{3} |y_{i}-y_{j}|
# 	&= 2\{(y_{2}-y_{1})+(y_{3}-y_{1})+(y_{3}-y_{2})\} \\
# 	&= 4(y_{3}-y_{1}) \\
# 	\bar{y} &= \frac{1}{3} (y_{1}+y_{2}+y_{3})
# \end{align*}
# より
# \begin{align*}
# 	G &= \frac{2}{3} \frac{y_{3}-y_{1}}{y_{1}+y_{2}+y_{3}}
# \end{align*}
# となる．

# 次に，面積からジニ係数を計算する．
# 横軸と縦軸の値はそれぞれ表\ref{tb:lorentz}のようになる．
# ローレンツ曲線と$ x=1 $，$ y=0 $に囲まれた領域の面積は1つの三角形と2つの台形から成るので，
# 
# \begin{align*}
# 	\frac{1}{2}\cdot\frac{1}{3} \left[\alpha_{1}+(\alpha_{1}+\alpha_{2})+(\alpha_{2}+1)\right]
# 	&= \frac{1}{6}(2\alpha_{1}+2\alpha_{2}+1)
# \end{align*}
# 
# これより，完全平等線と$ x=1 $，$ y=0 $に囲まれた領域の面積は
# 
# \begin{align*}
# 	\frac{1}{2} - \frac{1}{6}(2\alpha_{1}+2\alpha_{2}+1) = \frac{1}{3} (1-\alpha_{1}-\alpha_{2})
# \end{align*}
# 
# となるので，ジニ係数は
# 
# \begin{align*}
# 	G 
# 	&= \frac{1}{3} (1-\alpha_{1}-\alpha_{2}) \div \frac{1}{2} \\
# 	&= \frac{2}{3} (1-\alpha_{1}-\alpha_{2}) \\
# 	&= \frac{2}{3} \frac{y_{3}-y_{1}}{y_{1}+y_{2}+y_{3}}
# \end{align*}
# 
# と求まる．
# 
# 以上より，式{eq}`eq:gini`から求めたジニ係数と面積から求めたジニ係数が確かに一致することが分かった．
# なお，一般の$ n $に対する証明は省略する．

# In[5]:


x = np.array([25, 25, 25, 25])
X = np.cumsum(x) / np.sum(x)
y = np.array([15, 25, 40, 80])
Y = np.cumsum(y) / np.sum(y)


# In[6]:


pd.DataFrame(np.c_[x, X, y, Y],
             columns=['サイズ', 'サイズの累積相対度数', '平均所得', '所得の累積相対度数'])


# **Pythonによる実装**

# In[7]:


X2 = np.append(0, X)
Y2 = np.append(0, Y)


# In[8]:


fig, ax = plt.subplots()

ax.plot(X2, Y2, 'o--')
ax.plot([0, 1], [0, 1], '-')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel(u'サイズの累積相対度数')
ax.set_ylabel(u'所得の累積相対度数')
fig.savefig('./figure/lorentz.pdf', bbox_inches="tight", pad_inches=0.2, transparent=True, dpi=300)


# 面積から求める

# In[ ]:


S1 = 0.5  # 完全平等選，x軸，y軸で囲まれた三角形の面積
S2 = 0    # ローレンツ曲線，x軸，y軸で囲まれた面積
for (a, b, h) in zip(Y2[:-1], Y2[1:], np.diff(X2)):
    S2 += (a+b)*h/2
G = (S1 - S2) / S1


# In[ ]:


G


# 公式から求める

# In[ ]:


G = np.fabs(np.add.outer(y, -y)).sum() / np.mean(y) / 2 / len(y)**2
G


# ## 実例：地域の豊かさの格差は拡大しているか？

# ### STEP1: Problem
# 
# - 2015年の国勢調査では，日本全体の人口が1920年の調査開始以来，初めて減少したことが明らかになった．
# - また，都道府県ごとの人口を見ても，5年前（2010年）に比べて人口が減少したのは39の道府県にのぼる．
# - 一方，東京を中心とした大都市には人口が集中し，都市部と地方の格差が広がっているのも事実である．
# - 人口は経済・社会の基盤を成すものであり，人口の増減は経済的な豊かさと密接に関わっていると思われる．
# - 近年の人口変動によって，地域間で経済的な豊かさの格差は拡大したのだろうか？

# ### STEP2: Plan
# 
# - 地域ごとの経済的な豊かさを捉える指標として，都道府県別の1人当たり県民所得に着目する．
# - これは，企業を含めて県民全体の経済水準を表すもので，都道府県間で比較可能な統計データである．
# - ただし，各都道府県は人口規模が大きく異るので，地域ごとに比較する際は規模を表す人口等の変数で除した量を用いることが必要となる．
# - そこで，今回用いる1人当たり県民所得は，県民所得を県内に居住する人口（「国勢調査」と「人口推計」に準拠）で除して求める．
# - また，格差の大きさは一人当たり県民所得の標準偏差，変動係数，ジニ係数で評価し，ばらつきが40年間で拡大しているか否かを調べる．

# ### STEP3: Data
# 
# - 1人当たり県民所得は，内閣府「県民経済計算」(https://www.esri.cao.go.jp/jp/sna/data/data_list/kenmin/files/files_kenmin.html) から利用することができる．
# - ただし，年度が同じでも基準（平成23年基準や平成17年基準など）によって算出された値が異なることに注意する．

# In[9]:


PI = pd.read_csv('material/sec_2-2/prefectural_income.csv', index_col='p')
PI.columns = PI.columns.astype(int)
PI = np.round(PI/10, 0)  # 単位を万円に変換


# In[10]:


PI


# ### STEP4: Analysis

# **実習：平均と標準偏差**
# - 各年度に対して平均と標準偏差を求めよ．
# - 1975年〜91年の標準偏差は一貫して増加しており，格差は拡大しているように見えるが，本当にそう言えるか？平均値の変化と関連付けて考えよ．

# In[11]:


fig, ax = plt.subplots(figsize=(7, 3))
ax.set_xlabel('年度')

# 1人あたり県民所得の平均
ax.plot(PI.columns, PI.mean())
ax.set_ylim(0, 350)
ax.set_ylabel('平均（万円）')

# 1人あたり県民所得の標準偏差
ax2 = ax.twinx()
ax2.plot(PI.columns, PI.std(), 'r--')
ax2.set_ylim(0, 70)
ax2.set_ylabel('標準偏差（万円）', color='r')


# **実習：変動係数**
# - 全年度に対して変動係数を求め，時系列変化を可視化せよ．
# - 変動係数の変化から，1975年〜91年および全期間にかけて格差が増加しているか考えよ．

# In[ ]:


fig, ax = plt.subplots(figsize=(7, 3))
ax.set_xlabel('年度', fontname='IPAexGothic')

# 1人あたり県民所得の標準偏差
ax.plot(PI.columns, PI.std(), 'k-')
ax.set_ylim(0, 70)
ax.set_ylabel('標準偏差（万円）', fontname='IPAexGothic')

# 1人あたり県民所得の変動係数
ax2 = ax.twinx()
ax2.plot(PI.columns, PI.std()/PI.mean(), 'r--')
ax2.set_ylim(0, 0.2)
ax2.set_ylabel('変動係数', fontname='IPAexGothic', color='r')


# **実習：ローレンツ曲線，ジニ係数**
# - 年度を１つ選び，その年度のローレンツ曲線とジニ係数を求めよ．
# - 全年度に対してジニ係数を求め，時系列変化を可視化せよ．
# - ジニ係数の変化から，1975年〜91年および全期間にかけて格差が増加しているか考えよ．

# 2013年度のローレンツ曲線

# In[12]:


x = np.ones(47)
X = np.cumsum(x) / np.sum(x)
y = np.sort(PI[2013])
Y = np.cumsum(y) / np.sum(y)
X2 = np.append(0, X)
Y2 = np.append(0, Y)


# In[13]:


fig, ax = plt.subplots()

ax.plot(X2, Y2, '--')
ax.plot([0, 1], [0, 1], '-')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel(u'サイズの累積相対度数')
ax.set_ylabel(u'所得の累積相対度数')


# ジニ係数の時間変化

# In[15]:


G = []
for t in PI.columns:
    x = np.ones(47)
    X = np.cumsum(x) / np.sum(x)
    y = np.sort(PI[t])
    Y = np.cumsum(y) / np.sum(y)

    g = np.fabs(np.add.outer(y, -y)).sum() / np.mean(y) / 2 / len(y)**2
    G.append(g)


# In[16]:


fig, ax = plt.subplots(figsize=(7, 3))
ax.set_xlabel('年度')

# 1人あたり県民所得の変動係数
ax.plot(PI.columns, PI.std()/PI.mean(), 'k', label='変動係数')
ax.set_ylim(0.1, 0.2)
ax.set_ylabel('変動係数')

# ジニ係数
ax2 = ax.twinx()
ax2.plot(PI.columns, np.array(G), 'r--', label='ジニ係数')
ax2.set_ylim(0.05, 0.1)
ax2.set_ylabel('ジニ係数', color='r')


# ### STEP 5: Conclusion
# 
# - 格差を表す指標の40年間の推移から地域間で経済的な豊かさの格差が拡大したのかどうか考えよ．
# - 格差を表す指標の40年間の推移を見ると，細かい時間スケールでの変動が見られる．これらは具体的にどのような出来事を反映していると考えられるか？
