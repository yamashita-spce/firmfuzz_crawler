# FirmFuzz Crawler (Reimplementation)

このレポジトリは、ファームウェアファジングツールであるFirmFuzzのWebクローリング機能のみを抽出して再実装したものです。

## 主要な機能

- **Webページの自動認証**: デフォルトの認証情報（admin/password）を使用して、指定されたURLのWebページに自動的にログインを試みます。
- **URLスクレイピング**: ログイン後、Webページ内のリンク（`<a>`タグの`href`属性）を再帰的に収集します。
- **フレーム対応**: HTMLフレームセットを使用しているWebページにも対応し、各フレーム内のリンクもスクレイピングします。
- **属性オブジェクト作成**: スクレイピングされた各URLに対して、入力フィールド、ボタン、ラジオボタンなどの要素情報を保持する属性オブジェクトを作成します。

## 環境要件

- Python 2.7.18
- 以下のPythonパッケージ:
  - `requests`
  - `selenium`
  - `certifi`
  - `chardet`
  - `idna`
  - `urllib3`
  - `pip`
  - `setuptools`
  - `wheel`
- **ChromeDriver**: SeleniumがWebブラウザを操作するために必要です。お使いのChromeブラウザのバージョンに対応したChromeDriverをダウンロードし、システムパスが通っている場所、または`my_crawler/`ディレクトリに配置してください。

## セットアップ手順

1. **Python環境の構築**: pyenvを使用してPython 2.7.18環境を構築します。
   ```bash
   pyenv install 2.7.18
   pyenv local 2.7.18
   ```

2. **依存関係のインストール**: 必要なPythonパッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
   （注: `requirements.txt`ファイルは含まれていませんが、上記のパッケージリストを元に手動でインストールするか、`pip freeze > requirements.txt`で生成してください。）

3. **ChromeDriverの設定**: 前述の「環境要件」に従ってChromeDriverを配置します。

## 使用方法

クローラーを実行するには、以下のコマンドを使用します。

```bash
python my_crawler/crawler.py [オプション]
```

### オプション

- `-u <URL>`, `--url <URL>`: クローリングを開始するWebページのURLを指定します。デフォルトは `http://127.0.0.1:8080` です。

### 実行例

```bash
python my_crawler/crawler.py -u http://192.168.1.1
```

## プロジェクト構造

- `my_crawler/`: クローラーの主要な実装が含まれます。
  - `crawler.py`: メインの実行スクリプト。認証処理とスクレイピングの開始を担当します。
  - `my_mapper.py`: WebページからのURLスクレイピングロジックを実装しています。フレームの有無に応じて異なるクラス（`ScrapeFlatHref`, `ScrapeHrefWithFrames`）を提供します。
  - `my_attribute_obj.py`: スクレイピングされたURLの属性（入力フィールド、ボタンなど）を格納するためのクラスです。
- `src/`: 元のFirmFuzzプロジェクトのソースコードが含まれており、参考として利用できます。

## 設定

デフォルトの認証情報（admin/password）を変更したい場合は、`my_crawler/crawler.py` ファイル内の `LOGIN_NAME` および `LOGIN_PASSWORD` 変数を編集してください。

```python
LOGIN_NAME = "your_username"
LOGIN_PASSWORD = "your_password"
```

## 注意事項

- このプロジェクトはPython 2.7で動作します。Python 2.7は既にサポートが終了しているため、本番環境での使用は推奨されません。学習または研究目的での使用に限定してください。
- ChromeDriverのパスが正しく設定されていることを確認してください。設定されていない場合、Seleniumがブラウザを起動できずエラーが発生します。
- 認証処理は基本的なフォーム認証を想定しています。複雑な認証メカニズムには対応していない場合があります。
