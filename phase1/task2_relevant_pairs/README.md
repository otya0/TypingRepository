# Task 2: 関連商品ペアの分析

## 概要
同時に購入された商品のペアについて、その購入回数を集計し、関連性の高いペアを見つける。

## やるべきこと
- 各顧客の購買履歴から、同時に購入された全ての2商品の組み合わせを列挙する
- 各ペアについて、何人の顧客が同時に購入したかをカウントする
- ペア内では辞書順で小さい方を先に出力する
- 購入回数の降順でソート（同数の場合は辞書順）
- クエリ [a, b] に対して、a番目からb番目までのペア情報を出力する

## 入力形式
```
N                          ← 顧客数
M1 p1,1 p1,2 ... p1,M1    ← 購入商品数と商品名
...
Q                          ← クエリ数
a1 b1
...
```
（Task 1 と同じ形式。ただしクエリはペアに対するもの）

## 出力形式
各クエリに対して、購入回数とペアの商品名を1行ずつ出力する。
```
購入回数 商品名1 商品名2
```

## 制約
- 1 ≤ N ≤ 100, 1 ≤ M ≤ 10, 1 ≤ Q ≤ 10

## 入出力例

### 例1
入力:
```
6
3 tea butter bread
2 butter bread
3 onion carrot potato
2 rice onion
3 bread tea butter
5 water onion carrot potato rice
2
1 7
8 13
```
出力:
```
3 bread butter
2 bread tea
2 butter tea
2 carrot onion
2 carrot potato
2 onion potato
2 onion rice
1 carrot rice
1 carrot water
1 onion water
1 potato rice
1 potato water
1 rice water
```

## 必要なスキル
- アルゴリズム基礎（組み合わせの列挙）

## 実装のポイント
- `itertools.combinations` を使って各顧客の商品リストから全ペアを生成
- ペアを生成する前に商品名をソートしておけば、自動的に辞書順になる
- `defaultdict(int)` でペアの出現回数を効率よくカウント
