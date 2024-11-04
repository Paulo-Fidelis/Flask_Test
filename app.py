from flask import *
import sqlite3

app = Flask(__name__)


database = 'database.db'

# funcao que faz a conexao com o banco de dados
def getDb():
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    return db


# criador do banco de dados 
def init_db():
    with app.app_context():
        db = getDb()
        with app.open_resource('bdcreate.sql', mode='r') as bd: #essa mizera aqui abre o arquivo, não sei para que serve o 'mode', nem oq 'r' significa
            script = bd.read()  #precisa dessa variavel, pq? não faço a menor ideia
            db.cursor().executescript(script)
        db.commit()

# iniciador do flask, renderizando o Index
@app.route('/')
def home():
    return render_template('index.html')

#rota do flask que faz as inserções no banco de dados
@app.route('/criar', methods=['POST']) #nao sei oq post, ou get faz, quando um nao da certo, eu testo o outro
def criarFilme():
    nome = request.form['nome']
    autor = request.form['autor']
    desc = request.form['descricao']
    try: #não precisa de classe nem de lista, amém
        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO filme (nome, autor, descricao) VALUES (?,?,?)', (nome, autor, desc))#muito mais fácil que o alchemy
        db.commit()
    except sqlite3.Error as e:
        print('Falha na inserção dos dados') #se der erro fudeu, nao sei ajeitar, só sei que ta funcionando agr as 19:32 do dia 04/11/24
        print(e)
    finally:
        db.close()
        return redirect('/')
    

def getFilme(nome): #funcao que faz uma busca de id pelo banco de dados
    try:
        db = getDb()
        cursor = db.cursor() 
        cursor.execute('SELECT id FROM filme WHERE nome = ?', (nome, )) #NAO TIRA A CARALHA DA VIRGULA DPS DA VARIAVEL NOME, SE TIRAR DA ERRADO
        filme1 = cursor.fetchone()
        return filme1[0] #PARA DESCOBRIR QUE EU TINHA QUE PEGAR O INDICE 0 DESSA DESGRAÇA FOI O INFERNO NA TERRA, NÃO MEXE
    except sqlite3.Error as e:
        print('Falha na busca')
        print(e)
    finally:
        db.close() 


@app.route('/alterar', methods=['POST']) #função que altera os filmes
def alteracaoFilme():
    nome_antigo = request.form['nome_antigo'] #caçando o nome antigo e puxando o id logo em seguida
    identificador = getFilme(nome_antigo)
    nomeNovo = request.form['nome_novo']
    autorNovo = request.form['autor_novo']
    descNova = request.form['desc_nova']
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None: #fazendo uma validação se o identificador nao for nulo 
            cursor.execute('UPDATE filme SET nome = ?, autor = ?, descricao = ? WHERE id = ?', (nomeNovo, autorNovo, descNova, identificador))
        db.commit() #comitando no banco de dados o update
    except sqlite3.Error as e:
        print('Falha na busca')
        print(e)
    finally:
        db.close()
        return redirect('/')

@app.route('/deletar', methods=['POST']) #função para deletar o filme de acordo com o id
def deletarFilme():
    nomeDeletado = request.form['nome_delete']
    identificador = getFilme(nomeDeletado) #caçando o id do filme digitado
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None: #fazendo a mesma validação da atualização
            cursor.execute('DELETE FROM filme WHERE id = ?', (identificador, )) 
        db.commit() #comitando o delete
    except sqlite3.Error as e:
        print('Falha na busca')
        print(e)
    finally:
        db.close()
        return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', debug=True)