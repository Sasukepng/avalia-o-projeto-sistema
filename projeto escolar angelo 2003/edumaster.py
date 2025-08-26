from flask import Flask, request, redirect, url_for, render_template_string, jsonify

app = Flask(__name__)

# Simulação de banco de dados em memória
usuarios = {}  # {'usuario': {'senha': '123', 'painel': {...}}}

@app.route('/')
def home():
    return redirect(url_for('tela_login'))

@app.route('/login')
def tela_login():
    # Aqui você pode usar render_template se tiver um arquivo HTML separado
    return render_template_string('<h3>Use o formulário HTML que criamos anteriormente aqui.</h3>')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    acao = request.form['acao']

    if acao == 'cadastrar':
        if usuario in usuarios:
            return jsonify({'mensagem': 'Usuário já existe!'})
        usuarios[usuario] = {
            'senha': senha,
            'painel': {
                'notas': ['Matemática: 8.5', 'História: 9.0'],
                'turmas': ['1º Ano A', '2º Ano B']
            }
        }
        return jsonify({'mensagem': 'Cadastro realizado com sucesso!'})

    elif acao == 'login':
        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            return redirect(url_for('painel_usuario', usuario=usuario))
        return jsonify({'mensagem': 'Usuário ou senha incorretos.'})

    return jsonify({'mensagem': 'Ação inválida.'})

@app.route('/recuperar_senha', methods=['POST'])
def recuperar_senha():
    usuario = request.form['usuario']
    if usuario in usuarios:
        usuarios[usuario]['senha'] = 'nova_senha123'
        return jsonify({'mensagem': 'Senha redefinida para "nova_senha123". Altere após login.'})
    return jsonify({'mensagem': 'Usuário não encontrado.'})

@app.route('/painel/<usuario>')
def painel_usuario(usuario):
    if usuario in usuarios:
        painel = usuarios[usuario]['painel']
        return f"""
        <h2>Painel do Usuário: {usuario}</h2>
        <h4>📘 Notas:</h4>
        <ul>{"".join(f"<li>{nota}</li>" for nota in painel['notas'])}</ul>
        <h4>🏫 Turmas:</h4>
        <ul>{"".join(f"<li>{turma}</li>" for turma in painel['turmas'])}</ul>
        """
    return jsonify({'mensagem': 'Usuário não encontrado.'})

if __name__ == '__main__':
    app.run(debug=True)