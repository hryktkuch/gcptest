from flask import Flask, request, jsonify, render_template, redirect, url_for
from google.cloud import firestore
import os

app = Flask(__name__)

# Firestoreに接続
def get_firestore_client():
    if os.getenv('FLASK_ENV') == 'production':
        return firestore.Client()  # GCP環境ではデフォルト認証情報を使用
    else:
        return firestore.Client()

db = get_firestore_client()

# データ追加フォームとデータ表示のためのルート
@app.route('/')
def index():
    # Firestoreからデータを取得
    books_ref = db.collection('books')
    docs = books_ref.stream()

    books = []
    for doc in docs:
        books.append(doc.to_dict())

    # フロントエンドにデータを渡して表示
    return render_template('index.html', books=books)

# データの追加
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    
    # Firestoreに新しいドキュメントを追加
    doc_ref = db.collection('books').document()
    doc_ref.set({
        'title': title,
        'author': author
    })
    
    return redirect(url_for('index'))  # データ追加後にホームページにリダイレクト

if __name__ == '__main__':
    app.run(debug=True)
