library(RMeCab)
library(stringkernels)
library(kernlab)

# 初期化
{
    seed <- 100  # 乱数のseed

    data <- readLines("tweets.dat")

    # SVMlightのデータ形式からツイート部分だけ抽出
    tweets <- sub("-?1 #", "", data)

    # SVMlightのデータ形式のクラス情報からユーザ名を割り当てる
    user <- factor(ifelse(grepl("^1", data), "midoisan", "a_bicky"))

    # ホワイトスペースだけ、または、5文字未満のツイートを取り除く
    remove.index <- which(grepl("^\\s+$", tweets) | sapply(tweets, nchar) < 5)
    tweets <- tweets[-remove.index]
    user <- user[-remove.index]

    # 学習・テストを2対1の割合で設定
    set.seed(seed)
    train.index <- which(sample(seq(0, 1, len = 100), length(tweets), replace = TRUE) < 0.67)
    # 次のようなやり方だとデータが均等に分かれてベターだったかもしれない・・・
    # train.index <- unlist(suppressWarnings(split(1:length(tweets), 1:3))[1:2])
}

# Gap-weighted String Kernel (n = 2, lambda = 0.7)
{
    K <- gapweightkernel(2, 0.7, use_character = TRUE)

    # グラム行列を計算
    pre <- precomputedkernel(K, as.list(tweets), use_dummy = TRUE)

    # モデルを学習
    dummy <- precomputeddummy(tweets)
    model <- ksvm(dummy[train.index], user[train.index], kernel = pre)

    # クロス集計表の表示
    tbl <- table(true = user[-train.index], pred = predict(model, dummy[-train.index]))
    print(tbl)

    # 正解率
    print(sum(diag(tbl)) / sum(tbl))
}

# 文字 bigram
{
    # 文字・ツイート行列
    tweet.mat <- docNgramDF(tweets, type = 0, N = 2)

    # モデルを学習
    model <- ksvm(tweet.mat[train.index, ], user[train.index], kernel = vanilladot, kpar = list())

    # クロス集計表の表示
    tbl <- table(true = user[-train.index], pred = predict(model, tweet.mat[-train.index, ]))
    print(tbl)

    # 正解率
    print(sum(diag(tbl)) / sum(tbl))
}
