# djangoDockerApp
Set up a Django environment using Docker.

## Backend用の構成
Django REST Framework (DRF)は、PythonのWebフレームワーク「Django」上でRESTful APIを高速かつ効率的に構築するための強力なライブラリです。シリアライズ（データ変換）、認証、URLルーティング機能などを提供し、SPA（React/Vue）やモバイルアプリのバックエンド開発に最適です。 

https://youtu.be/J4O76oInjIU?si=ndJu5RrK3KhPilN-

**DRFの主な特徴とメリット**

* シリアライザー（Serializer）: データベースのモデルやPythonオブジェクトを、JSON形式などのWebで扱いやすいデータに変換・バリデーションする核心機能。
* 高速開発: ViewSetとRouterを使用することで、CRUD（作成、読み出し、更新、削除）APIを数行のコードで自動生成できる。
* 強力な認証・権限管理: OAuth, JWT, トークン認証などが標準でサポートされており、安全なAPI構築が可能。
* ドキュメント自動生成: drf-spectacularなどのライブラリを組み合わせ、API仕様書（Swagger/OpenAPI）を自動生成できる。 

https://youtu.be/RWORU-FD4Ss?si=AhCklp650NuXcrW2

通常のDjangoとの違い
Django: サーバー側でHTMLを生成する（SSR）フルスタックWebアプリ向け。
DRF: JSONデータのみをやり取りするAPIサーバー向け。 
Zenn
Zenn
 +1
基本的な構成要素
Serializer: データの変換
ViewSets/Views: ビジネスロジックの処理
Routers: URLパターンの自動ルーティング 
Zenn
Zenn
 +2
モダンなバックエンドAPI開発において、Python環境ではデファクトスタンダード（事実上の標準）となっているフレームワークです。