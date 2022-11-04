#!/usr/bin/env python
# coding: utf-8

# In[7]:


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
pd.set_option('display.max_columns', 10)  # 表示する行数
get_ipython().run_line_magic('precision', '3')


# # 特性値の活用

# 量的データが与えられたとき，まず行うべきことはヒストグラムを描いてデータの分布（どの値がどの程度あるか）を把握することである．
# その上で，分布形状が単峰性であれば，データから計算した少数の指標によってデータを要約することができる．
# このように，データの特性を定量的に表すための指標を**特性値**（あるいは代表値，記述統計量，ようやく統計量）と呼ぶ．
# 一般にデータの特性はデータの中心を表す特性値とデータの中心からのばらつきを表す特性値によって要約される．
# 
# ※ データの分布形状が多峰性の場合に中心＋ばらつきのように少数の指標で要約すると，データの特性をうまく表すことができない．

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

# **Pythonによる実装**
# 
# まずはアヤメデータを読み込む．

# In[23]:


# アヤメデータをPandasに読み込む
Iris = pd.read_csv('./Iris.csv')
Iris = Iris.iloc[:, 1:5]
Iris.columns=['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']


# このデータに対し，式{eq}`eq:arithmetic_mean`を当てはめれば算術平均を計算することができる．
# 例えば，アヤメのがく片の幅（Sepal Width）のデータの場合，平均値は$ \bar{x}=3.054 $ cm，アヤメの花弁の幅（Petal Width）のデータの場合，平均値は$ \bar{x}=1.199 $ cmとなる．

# In[19]:


# アヤメのがく片の長さの平均（Pandasのmeanメソッドを用いる）
print('がく片の幅の平均', Iris['Sepal Width'].mean())
print('花弁の幅の平均', Iris['Petal Width'].mean())


# 以下はがく片の幅（Sepal Width）と花弁の幅（Petal Width）のヒストグラム上に平均値を示した図である．
# がく片の幅についてはヒストグラムが単峰性で左右対称となるため，平均値がデータの中心にほぼ一致していることが分かる．
# 一方，花弁の幅についてはヒストグラムが双峰性となるため，平均値だけを見るとデータの特性を見誤る恐れがある．
# このような場合を想定し，データが与えられたらまずはヒストグラムを確認することが重要である．
# 

# In[22]:


# ビンの個数（スタージェスの公式）
bn = int(1+np.log2(len(Iris)))

# ヒストグラムの描画と保存
for i in ['Sepal Width', 'Petal Width']:
    fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)

    # 平均値の位置
    ave = Iris[i].mean()
    ax.plot([ave, ave], [0, 100], 'r-')
    
    x = ax.hist(Iris[i], # データ
                bins=int(bn), # 階級数
                histtype='bar',  # ヒストグラムの種類
                color='c', ec='k', alpha=0.5  # 縦棒の色，透明度
               )[1]
    x2 = np.round(0.5*(x[1:]+x[:-1]), 2)  # 横軸に表示する階級値（中央値）
    
    ax.set_title(i)  # グラフのタイトル
    ax.set_xticks(x2) # 横軸の目盛り
    ax.set_xticklabels(x2, fontsize=8) # 横軸の目盛り
    ax.set_xlabel(i+' [cm]')  # 横軸のラベル
    ax.set_ylabel('Frequency') # 縦軸のラベル
    ax.set_ylim(0, 45)


# ### 幾何平均

# 算術平均は平均の計算方法として最も一般的であるが，それ以外の方法もある．
# それが**幾何平均**である．
# 幾何平均は，$ n $個のデータに対して，全ての値の積の$ n $乗根をとったもので，
# 
# $$
# 	\bar{x}_{g} = \sqrt[n]{x_{1}\times\cdots \times x_{n}} = \sqrt[n]{\prod_{i=1}^{n}x_{i}} = \left(\prod_{i=1}^{n}x_{i}\right)^{1/n}
# $$(eq:geometric_mean)
# 
# と定義される．
# ルートを取っているので，幾何平均は正の数のみしか扱えず，さらに掛け算によって定義されるので比率データにしか適用できない．

# 幾何平均は成長率や倍率の平均を計算するときに用いられる．
# 例えば，次のような事例を考える：
# 
# > 1年目から2年目にかけての物価は対前年比2倍になり（100円のものが200円になり），2年目から3年目にかけての物価は対前年比8倍となった（200円のものが1600円になった）．
# >では，この2年間の物価の対前年比伸び率の平均はいくらか？
# 
# まず，算術平均を適用してみる．
# すると，物価の対前年比伸び率の平均は$ (2+8)/2=5 $倍となる．
# これは，1年目に100円だったものが2年目に500円になり，さらに3年目に2500円になることを意味するので，実際よりも過大に見積もってしまう．
# そこで，次に幾何平均を適用してみる．
# すると，物価の対前年比伸び率の平均は$ \sqrt[2]{2\times 8}=4 $倍となる．
# これは，1年目に100円だったものが2年目に400円になり，さらに3年目に1600円になることを意味するので，実際の金額と一致する．
# このように，倍率の平均値を計算する場合には，算術平均ではなく幾何平均を用いるのが妥当である．

# **Pythonによる実装**

# 幾何平均の定義をそのまま適用すると，全データの積を計算する必要がありその結果が巨大な数となる可能性がある．
# この場合，オーバーフローを起こすことがあるので，以下のように対数を取ってから算術平均を計算し，最後に元に戻すとうまくいく．

# In[23]:


x = np.log(Iris['Sepal Length'])
np.exp(np.sum(x)/len(x))


# 以下のように`scipy`を使う方法もある．

# In[24]:


from scipy.stats.mstats import gmean
gmean(Iris['Sepal Length'])


# ### 中央値

# データの分布形状が単峰性であっても左右非対称である場合，算術平均はデータの中心を表す特性値としてふさわしくない．
# 例えば，
# 
# $$
# 	1,1,1,1,2,3,4,5,16,20 
# $$
# 
# のようなデータがあったとき，この算術平均は5.4になるが，平均より小さいものが8個を占め，残りの2個が平均より大きい．
# これは，少数のデータ（16と20）が平均を押し上げている例である．
# このような場合，分布の中心という意味では既に述べた**中央値**（メディアン）を用いる方が適切である．
# 実際，中央値を用いれば，その値より小さい数と大きい数の個数が等しくなる．

# **Pythonによる実装**

# In[24]:


# 最頻値の計算（Pandasのmedianメソッドを用いる）
Iris['Sepal Length'].median()


# ### 最頻値

# 平均値，中央値の他によく用いられる特性値として，**最頻値**（モード）がある．
# これは，データの中で最も頻出する数であり，度数分布において度数が最大となる階級の階級値に対応する．
# 分布形状が単峰性で左右非対称な場合には，データの中心を表す特性値としてよく用いられる．
# ただし，分布形状が双峰性の場合には有効な特性値とならないので注意が必要である．

# **Pythonによる実装**

# In[25]:


# 最頻値の計算（Pandasのmodeメソッドを用いる）
Iris['Sepal Length'].mode()


# ## データのばらつきを表す特性値

# データの特性を知りたい場合，中心を表す特性値だけでは情報不足であり，中心からどの程度ばらついているかも考慮しなければならない．
# 例えば，以下の3つのデータは中心を表す算術平均，中央値，最頻値がすべて5であるが，分布の形状は異なる．
# 
# - A: $0,3,3,5,5,5,5,7,7,10$
# - B: $0,1,2,3,5,5,7,8,9,10$
# - C: $3,4,4,5,5,5,5,6,6,7$

# 通常，ばらつきを求める際には，算術平均と各データとの差$ x_{i} - \bar{x} $を考える．
# これを**偏差**と呼ぶ．
# この偏差を全データに対して平均すれば，ばらつきを表す特性値になりそうであるが，これだと問題が生じる．
# 例えば，データが左右対称に分布している場合，平均より小さい値のデータ（偏差が負）と大きい値のデータ（偏差が正）が同程度あるため，偏差を平均するとほぼ0になってしまう．
# ばらつきが0というのは明らかにおかしいため，別の特性値を考える必要がある．
# 以下に代表的な方法を説明する．

# ### 平均偏差

# １つ目の方法は偏差の絶対値を取ってから平均するという方法であり，**平均偏差**と呼ばれる：
# 
# $$
# 	平均偏差 = \frac{1}{n} \sum_{i=1}^{n}|x_{i}-\bar{x}| 
# $$(eq:mean_deviation)
# 
# これは，$ n $個のデータの偏差の絶対値を平均した値であり，ばらつきの指標として直感的に理解しやすい．
# しかし，絶対値の扱いが数学的に面倒，分布の中心が$ \bar{x} $ではなく中央値のときに最小になる，平均から大きく外れた値も等しい寄与となる，など問題があるため利用されることは少ない．

# **Pythonによる実装**

# In[32]:


np.fabs(Iris['Sepal Length'] - Iris['Sepal Length'].mean()).mean()


# ### 分散・標準偏差

# ２つ目の方法は，偏差を２乗してから平均するという方法であり，**分散**と呼ばれる：
# 
# $$
# 	s^{2} = \frac{1}{n} \sum_{i=1}^{n} (x_{i} - \bar{x})^{2}
# $$(eq:deviation)
# 
# 分散は$ n $個のデータの偏差の２乗を平均した値であり，平均値から大きく離れたデータほど寄与が大きくなる．
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

# In[30]:


# 分散
Iris['Sepal Length'].var()


# In[31]:


# 標準偏差
Iris['Sepal Length'].std()


# ### 変動係数

# 日本人男性の身長のデータは，平均値が約170cm，標準偏差が約6cmである．
# 一方，身長の単位をmで表すと，平均値は1.7m，標準偏差は0.06mとなる．
# このように，標準偏差は測定単位によって値が変化してしまう．
# また，標準偏差はデータの水準の変化（おおまかには平均値の大きさ）によっても大きさが変化する．
# 例えば，サイズの非常に小さい昆虫の場合には，サイズの平均値や標準偏差は人間の身長の場合よりも非常に小さくなるだろう．
# 
# 以上のように単位やデータの水準が異なる場合でも，データの分布形状がよく似ていれば平均値からのばらつきの程度を同じ指標で比較することが可能である．
# このためには，以下で定義される**変動係数**（Coefficient of Variation）を用いる：
# 
# $$
# 	\mathrm{CV} = \frac{s}{\bar{x}}
# $$(eq:cv)
# 
# 変動係数はデータの標準偏差を平均値で割った量である．
# 同じ単位を持つ量同士で割り算をしているので，無次元（単位がない）となり，データの測定単位に依らない．
# また，データの水準を表す平均値で割っているので，データの水準にも依らない．
# よって，通常，単位や平均値が異なるグループ間でばらつきを比較する際には変動係数がよく用いられる．

# **Pythonによる実装**

# In[29]:


Iris['Sepal Length'].std()/Iris['Sepal Length'].mean()


# ## ローレンツ曲線とジニ係数

# ### ローレンツ曲線

# ある集団を構成するメンバー（人物でも市町村でも何でも良い）に対し，ある量（所得や人口など）が対応したデータを考える．
# 以下では，各人物に対して所得が対応したデータを考えよう．
# 
# まず，各人物を所得の小さい順に並べて$ n $個の階級に分ける．
# その上で，下から$ i $番目の階級の度数（人数）を$ x_{i} $，累積相対度数を$ X_{i} $とする．
# ここで，累積相対度数$ X_{i} $とは，下から$ i $までの階級に属する人物が全体に占める割合である．
# 同様にして，階級$ i $の平均所得を$ y_{i} $，平均所得の累積相対度数を$ Y_{i} $とする．
# この場合，$ Y_{i} $は下から$ i $までの階級の平均所得が全体に占める割合となる．
# 
# 例えば，100人の集団を4階級（$n=4$）に分けた場合は以下のようになる．

# In[44]:


x = np.array([25, 25, 25, 25])
X = np.cumsum(x) / np.sum(x)
y = np.array([15, 25, 40, 80])
Y = np.cumsum(y) / np.sum(y)


# In[51]:


pd.DataFrame(np.c_[x, X, y, Y],
             columns=['度数xi', '累積相対度数Xi', '平均所得yi', '所得の累積相対度数Yi'],
             index=[1,2,3,4])


# 次に，以上を踏まえて横軸に累積相対度数$ X_{i} $，縦軸に平均所得の累積相対度数$ Y_{i} $を取ったグラフを考える．
# このグラフは**ローレンツ曲線**と呼ばれる．
# ローレンツ曲線の横軸，縦軸はともに0から1の範囲であり，必ず両端が$ (0, 0) $と$ (1, 1) $の折れ線グラフとなる．
# ローレンツ曲線上の$ (X, Y) $という点は，社会全体の貧しい側から$ X\times100 $\%の人が全体の$ Y\times100 $\%の所得を占めることを表す．
# 例えば，$ (0.25, 0.1) $という点は，社会全体の25\%の人が10\%の富を占めるということを表す．
# もし，所得が全人物に平等に配分されている場合，ローレンツ曲線は傾き1の直線となり，これを**完全平等線**と呼ぶ．
# 一方，所得の配分に格差があるほどローレンツ曲線は完全平等線から下にずれていく．
# このように，ローレンツ曲線はある社会における所得の配分格差を可視化したグラフといえる．

# In[50]:


fig, ax = plt.subplots(figsize=(5, 4))

X2 = np.append(0, X)
Y2 = np.append(0, Y)
ax.plot(X2, Y2, 'o--')
ax.plot([0, 1], [0, 1], '-')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel(u'サイズの累積相対度数', fontsize=15)
ax.set_ylabel(u'所得の累積相対度数', fontsize=15);
# fig.savefig('./figure/lorentz.pdf', bbox_inches="tight", pad_inches=0.2, transparent=True, dpi=300)


# ### ジニ係数

# 社会の格差の度合いはローレンツ曲線が完全平等線から下にずれるほど大きくなる．
# よって，ローレンツ曲線と完全平等線によって囲まれた部分の面積が，完全平等線，$ x=1 $，$ y=0 $で構成される三角形の面積に占める割合を格差の指標と考えることができる．
# この指標は**ジニ係数**と呼ばれる．

# 階級を$ n $等分したとき，下から$ i $番目の階級の平均所得を$ y_{i} $とする（$ y_{1}\leq y_{2} \leq \cdots \leq y_{n} $）．
# このとき，ジニ係数を以下のように表すことができる：
# 
# $$
# 	G = \frac{1}{2n^{2} \bar{y}} \sum_{i=1}^{n} \sum_{j=1}^{n} |y_{i} - y_{j}|
# $$(eq:gini)
# 
# ただし，$ \bar{y} = \frac{1}{n} \sum_{i=1}^{n} y_{i} $は全体の平均所得である．
# ジニ係数は0から1の間で定義され，完全に平等な配分のときに$ G=0 $，一人がすべての所得を占有しているときに$ G=(n-1)/n $となる（つまり$ n $が大きいときには1に近づく）．

# ```{admonition} 例）$ n=3 $ の場合の証明
# :class: dropdown
# 
# まず，式{eq}`eq:gini`を用いてジニ係数を計算すると，
# \begin{align*}
# 	\bar{y} &= \frac{1}{3} (y_{1}+y_{2}+y_{3}) \\
# 	\sum_{i=1}^{3}\sum_{j=1}^{3} |y_{i}-y_{j}|
# 	&= 2\{(y_{2}-y_{1})+(y_{3}-y_{1})+(y_{3}-y_{2})\} \\
# 	&= 4(y_{3}-y_{1}) 
# \end{align*}
# より
# \begin{align*}
# 	G &= \frac{2}{3} \frac{y_{3}-y_{1}}{y_{1}+y_{2}+y_{3}}
# \end{align*}
# となる．
# 
# 次に，面積からジニ係数を計算する．
# ローレンツ曲線の横軸と縦軸の値はそれぞれ{numref}`tb:n=3`のようになる．
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
# 
# ```

# ```{table} $ n=3 $の場合の度数分布表
# :name: tb:n=3
# |  階級  | 累積相対度数（横軸） | 所得の累積相対度数（縦軸） |
# | :---: | :---: | :---: |
# | 1    |  $1/3$ | $\alpha_{1}=\frac{y_{1}}{y_{1}+y_{2}+y_{3}}$ |
# | 2   | $2/3$ | $\alpha_{1}=\frac{y_{1}+y_{2}}{y_{1}+y_{2}+y_{3}}$ |
# | 3  | $1$ | 1 |
# ```

# **Pythonによる実装**

# In[39]:


# 面積から求める
S1 = 0.5  # 完全平等選，x軸，y軸で囲まれた三角形の面積
S2 = 0    # ローレンツ曲線，x軸，y軸で囲まれた面積
for (a, b, h) in zip(Y2[:-1], Y2[1:], np.diff(X2)):
    S2 += (a+b)*h/2
G = (S1 - S2) / S1
G


# In[40]:


# 公式から求める
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

# In[65]:


PI = pd.read_csv('prefectural_income.csv', index_col='p')
PI.columns = PI.columns.astype(int)
PI = np.round(PI/10, 0)  # 単位を万円に変換
PI


# ### STEP4: Analysis

# **実習：平均と標準偏差**
# - 各年度に対して平均と標準偏差を求めよ．
# - 1975年〜91年の標準偏差は一貫して増加しており，格差は拡大しているように見えるが，本当にそう言えるか？平均値の変化と関連付けて考えよ．

# In[54]:


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

# In[55]:


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

# In[56]:


x = np.ones(47)
X = np.cumsum(x) / np.sum(x)
y = np.sort(PI[2013])
Y = np.cumsum(y) / np.sum(y)
X2 = np.append(0, X)
Y2 = np.append(0, Y)


# In[57]:


fig, ax = plt.subplots()

ax.plot(X2, Y2, '--')
ax.plot([0, 1], [0, 1], '-')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel(u'サイズの累積相対度数')
ax.set_ylabel(u'所得の累積相対度数')


# ジニ係数の時間変化

# In[58]:


G = []
for t in PI.columns:
    x = np.ones(47)
    X = np.cumsum(x) / np.sum(x)
    y = np.sort(PI[t])
    Y = np.cumsum(y) / np.sum(y)

    g = np.fabs(np.add.outer(y, -y)).sum() / np.mean(y) / 2 / len(y)**2
    G.append(g)


# In[59]:


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
