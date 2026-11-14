"""
Banco de perguntas variadas para o Quiz Multiplayer.
Categorias:
- 🌍 Cultura Geral
- 🔬 Ciência & Tecnologia
- 🏛️ História & Geografia
- 🎬 Cinema & Séries
- ⚽ Esportes
- 🎮 Games & Pop
"""

import random

CATEGORIES = [
    "Todas as Categorias",
    "🌍 Cultura Geral",
    "🔬 Ciência & Tecnologia",
    "🏛️ História & Geografia",
    "🎬 Cinema & Séries",
    "⚽ Esportes",
    "🎮 Games & Pop"
]

ALL_QUESTIONS = [
    # 🌍 Cultura Geral
    {
        "id": 1,
        "categoria": "🌍 Cultura Geral",
        "pergunta": "Qual é a língua mais falada no mundo em número de falantes nativos?",
        "opcoes": ["Mandarim", "Inglês", "Espanhol", "Hindi"],
        "resposta": "Mandarim",
        "explicacao": "O mandarim possui cerca de 920 milhões de falantes nativos, superando o espanhol e o inglês."
    },
    {
        "id": 2,
        "categoria": "🌍 Cultura Geral",
        "pergunta": "Qual pintor é famoso por cortar a própria orelha?",
        "opcoes": ["Pablo Picasso", "Vincent van Gogh", "Claude Monet", "Salvador Dalí"],
        "resposta": "Vincent van Gogh",
        "explicacao": "Vincent van Gogh cortou parte de sua orelha esquerda em dezembro de 1888 em Arles, França."
    },
    {
        "id": 3,
        "categoria": "🌍 Cultura Geral",
        "pergunta": "Qual país tem o formato que se assemelha a uma bota no mapa?",
        "opcoes": ["Espanha", "Grécia", "Itália", "Portugal"],
        "resposta": "Itália",
        "explicacao": "A península itálica tem um formato característico de bota com salto alto no mar Mediterrâneo."
    },
    {
        "id": 4,
        "categoria": "🌍 Cultura Geral",
        "pergunta": "Quantas cores tem o arco-íris tradicionalmente?",
        "opcoes": ["5", "6", "7", "8"],
        "resposta": "7",
        "explicacao": "As 7 cores tradicionais descritas por Isaac Newton são: vermelho, laranja, amarelo, verde, azul, anil e violeta."
    },
    {
        "id": 5,
        "categoria": "🌍 Cultura Geral",
        "pergunta": "Em qual país foi inventado o papel?",
        "opcoes": ["Egito", "China", "Grécia", "Japão"],
        "resposta": "China",
        "explicacao": "O papel foi inventado na China por volta de 105 d.C. durante a dinastia Han por Cai Lun."
    },
    {
        "id": 6,
        "categoria": "🌍 Cultura Geral",
        "pergunta": "Qual é o livro mais vendido de todos os tempos depois da Bíblia?",
        "opcoes": ["Dom Quixote", "O Senhor dos Anéis", "O Pequeno Príncipe", "Harry Potter e a Pedra Filosofal"],
        "resposta": "Dom Quixote",
        "explicacao": "Estima-se que 'Dom Quixote' de Miguel de Cervantes já tenha ultrapassado 500 milhões de cópias vendidas."
    },

    # 🔬 Ciência & Tecnologia
    {
        "id": 7,
        "categoria": "🔬 Ciência & Tecnologia",
        "pergunta": "Qual elemento químico tem como símbolo 'Au' na tabela periódica?",
        "opcoes": ["Prata", "Ouro", "Cobre", "Alumínio"],
        "resposta": "Ouro",
        "explicacao": "Au vem do latim 'Aurum', que significa 'ouro brilhante'."
    },
    {
        "id": 8,
        "categoria": "🔬 Ciência & Tecnologia",
        "pergunta": "Qual planeta do Sistema Solar é conhecido como o 'Planeta Vermelho'?",
        "opcoes": ["Vênus", "Marte", "Júpiter", "Mercúrio"],
        "resposta": "Marte",
        "explicacao": "Marte tem aparência avermelhada devido à grande quantidade de óxido de ferro (ferrugem) em sua superfície."
    },
    {
        "id": 9,
        "categoria": "🔬 Ciência & Tecnologia",
        "pergunta": "Quem formulou a Teoria da Relatividade Geral?",
        "opcoes": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Stephen Hawking"],
        "resposta": "Albert Einstein",
        "explicacao": "Albert Einstein publicou a Teoria da Relatividade Geral em 1915."
    },
    {
        "id": 10,
        "categoria": "🔬 Ciência & Tecnologia",
        "pergunta": "Qual é a velocidade aproximada da luz no vácuo?",
        "opcoes": ["150.000 km/s", "300.000 km/s", "500.000 km/s", "1.000.000 km/s"],
        "resposta": "300.000 km/s",
        "explicacao": "A velocidade exata da luz no vácuo é de 299.792.458 metros por segundo (aprox. 300.000 km/s)."
    },
    {
        "id": 11,
        "categoria": "🔬 Ciência & Tecnologia",
        "pergunta": "Qual componente é considerado o 'cérebro' de um computador?",
        "opcoes": ["Memória RAM", "Processador (CPU)", "Placa de Vídeo (GPU)", "Disco Rígido (SSD)"],
        "resposta": "Processador (CPU)",
        "explicacao": "A CPU (Central Processing Unit) executa as instruções e cálculos lógicos centrais do sistema."
    },
    {
        "id": 12,
        "categoria": "🔬 Ciência & Tecnologia",
        "pergunta": "Qual é a molécula que carrega as instruções genéticas nos seres vivos?",
        "opcoes": ["RNA", "Proteína", "DNA", "Glicose"],
        "resposta": "DNA",
        "explicacao": "O Ácido Desoxirribonucleico (DNA) armazena todas as informações genéticas dos organismos vivos."
    },

    # 🏛️ História & Geografia
    {
        "id": 13,
        "categoria": "🏛️ História & Geografia",
        "pergunta": "Em que ano ocorreu a Proclamação da República no Brasil?",
        "opcoes": ["1822", "1889", "1930", "1500"],
        "resposta": "1889",
        "explicacao": "A República foi proclamada em 15 de novembro de 1889 pelo Marechal Deodoro da Fonseca."
    },
    {
        "id": 14,
        "categoria": "🏛️ História & Geografia",
        "pergunta": "Qual é o maior oceano da Terra em área de superfície?",
        "opcoes": ["Atlântico", "Índico", "Pacífico", "Ártico"],
        "resposta": "Pacífico",
        "explicacao": "O Oceano Pacífico cobre mais de 30% da superfície terrestre e supera a área combinada de todas as massas terrestres."
    },
    {
        "id": 15,
        "categoria": "🏛️ História & Geografia",
        "pergunta": "Qual país sediou as Olimpíadas da Antiguidade?",
        "opcoes": ["Itália", "Egito", "Grécia", "Turquia"],
        "resposta": "Grécia",
        "explicacao": "Os Jogos Olímpicos da Antiguidade nasceram na cidade grega de Olímpia por volta de 776 a.C."
    },
    {
        "id": 16,
        "categoria": "🏛️ História & Geografia",
        "pergunta": "Qual é a capital oficial da Austrália?",
        "opcoes": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "resposta": "Canberra",
        "explicacao": "Canberra foi escolhida em 1908 como um meio-termo conciliatório entre Sydney e Melbourne."
    },
    {
        "id": 17,
        "categoria": "🏛️ História & Geografia",
        "pergunta": "Quem foi o primeiro presidente da República dos Estados Unidos?",
        "opcoes": ["Thomas Jefferson", "George Washington", "Abraham Lincoln", "Benjamin Franklin"],
        "resposta": "George Washington",
        "explicacao": "George Washington liderou a Guerra Revolucionária e foi o primeiro presidente dos EUA de 1789 a 1797."
    },
    {
        "id": 18,
        "categoria": "🏛️ História & Geografia",
        "pergunta": "Qual cordilheira abriga o Monte Everest, o ponto mais alto da Terra?",
        "opcoes": ["Andes", "Alpes", "Himalaia", "Montanhas Rochosas"],
        "resposta": "Himalaia",
        "explicacao": "O Monte Everest (8.848m) fica no Himalaia, na fronteira entre Nepal e a China (Tibete)."
    },

    # 🎬 Cinema & Séries
    {
        "id": 19,
        "categoria": "🎬 Cinema & Séries",
        "pergunta": "Qual filme venceu o Oscar de Melhor Filme em 1998 e conta a história de um famoso naufrágio?",
        "opcoes": ["Titanic", "O Resgate do Soldado Ryan", "Gladiador", "Coração Valente"],
        "resposta": "Titanic",
        "explicacao": "Titanic, dirigido por James Cameron, venceu 11 estatuetas do Oscar no ano de 1998."
    },
    {
        "id": 20,
        "categoria": "🎬 Cinema & Séries",
        "pergunta": "Qual é o nome da escola de magia frequentada por Harry Potter?",
        "opcoes": ["Ilvermorny", "Hogwarts", "Beauxbatons", "Durmstrang"],
        "resposta": "Hogwarts",
        "explicacao": "Hogwarts é a Escola de Magia e Bruxaria do universo criado por J.K. Rowling."
    },
    {
        "id": 21,
        "categoria": "🎬 Cinema & Séries",
        "pergunta": "Quem dirigiu filmes clássicos como 'Pulp Fiction' e 'Kill Bill'?",
        "opcoes": ["Martin Scorsese", "Quentin Tarantino", "Christopher Nolan", "Steven Spielberg"],
        "resposta": "Quentin Tarantino",
        "explicacao": "Quentin Tarantino é o aclamado diretor e roteirista dessas obras cultuadas."
    },
    {
        "id": 22,
        "categoria": "🎬 Cinema & Séries",
        "pergunta": "Na série 'Breaking Bad', qual era a profissão original de Walter White antes de fabricar metanfetamina?",
        "opcoes": ["Advogado criminal", "Professor de Química", "Policial federal", "Médico oncologista"],
        "resposta": "Professor de Química",
        "explicacao": "Walter White lecionava química no ensino médio antes do diagnóstico de câncer."
    },
    {
        "id": 23,
        "categoria": "🎬 Cinema & Séries",
        "pergunta": "Qual super-herói bilionário usa o alter ego Bruce Wayne?",
        "opcoes": ["Homem de Ferro", "Batman", "Arqueiro Verde", "Demolidor"],
        "resposta": "Batman",
        "explicacao": "Bruce Wayne é o vigilante mascarado de Gotham City, o Batman."
    },
    {
        "id": 24,
        "categoria": "🎬 Cinema & Séries",
        "pergunta": "Qual é a famosa frase de Darth Vader para Luke Skywalker em 'O Império Contra-Ataca'?",
        "opcoes": ["'Luke, eu sou seu pai'", "'Não, eu sou seu pai'", "'Eu sou o seu criador'", "'Você é meu filho'"],
        "resposta": "'Não, eu sou seu pai'",
        "explicacao": "A linha exata proferida é 'No, I am your father' (Frequentemente lembrada errado como 'Luke, I am your father')."
    },

    # ⚽ Esportes
    {
        "id": 25,
        "categoria": "⚽ Esportes",
        "pergunta": "Qual país venceu o maior número de Copas do Mundo de Futebol masculino?",
        "opcoes": ["Alemanha", "Itália", "Brasil", "Argentina"],
        "resposta": "Brasil",
        "explicacao": "O Brasil é pentacampeão mundial (1958, 1962, 1970, 1994 e 2002)."
    },
    {
        "id": 26,
        "categoria": "⚽ Esportes",
        "pergunta": "Quantos jogadores compõem uma equipe de basquete em quadra durante o jogo?",
        "opcoes": ["4", "5", "6", "7"],
        "resposta": "5",
        "explicacao": "Cada time tem 5 jogadores em quadra simultaneamente no basquetebol."
    },
    {
        "id": 27,
        "categoria": "⚽ Esportes",
        "pergunta": "Qual atleta velocista jamaicano é o recordista mundial dos 100 metros rasos?",
        "opcoes": ["Tyson Gay", "Carl Lewis", "Usain Bolt", "Yohan Blake"],
        "resposta": "Usain Bolt",
        "explicacao": "Usain Bolt cravou o recorde mundial dos 100m em 9,58 segundos em Berlim (2009)."
    },
    {
        "id": 28,
        "categoria": "⚽ Esportes",
        "pergunta": "Em qual esporte se usa o termo 'strike' quando se derrubam todos os pinos de primeira?",
        "opcoes": ["Boliche", "Beisebol", "Sinuca", "Tênis"],
        "resposta": "Boliche",
        "explicacao": "No boliche, derrubar os 10 pinos no primeiro arremesso da rodada é chamado de strike."
    },
    {
        "id": 29,
        "categoria": "⚽ Esportes",
        "pergunta": "Quantas voltas tem uma prova padrão de 400 metros rasos em uma pista de atletismo?",
        "opcoes": ["Meia volta", "1 volta", "2 voltas", "4 voltas"],
        "resposta": "1 volta",
        "explicacao": "A raia 1 de uma pista oficial de atletismo tem exatamente 400 metros de extensão."
    },
    {
        "id": 30,
        "categoria": "⚽ Esportes",
        "pergunta": "Qual tenista suíço conquistou 20 títulos de Grand Slam e é considerado um dos maiores da história?",
        "opcoes": ["Rafael Nadal", "Novak Djokovic", "Roger Federer", "Andy Murray"],
        "resposta": "Roger Federer",
        "explicacao": "Roger Federer foi o primeiro homem a alcançar 20 títulos de Grand Slam no tênis moderno."
    },

    # 🎮 Games & Pop
    {
        "id": 31,
        "categoria": "🎮 Games & Pop",
        "pergunta": "Qual é a profissão do personagem Mario nos jogos clássicos da Nintendo?",
        "opcoes": ["Carpinteiro", "Encanador", "Eletricista", "Padeiro"],
        "resposta": "Encanador",
        "explicacao": "Apesar de ter começado como carpinteiro em Donkey Kong (Jumpman), Mario consagrou-se como encanador."
    },
    {
        "id": 32,
        "categoria": "🎮 Games & Pop",
        "pergunta": "Qual jogo eletrônico em blocos de montar criado por 'Notch' se tornou o mais vendido da história?",
        "opcoes": ["Roblox", "Minecraft", "Terraria", "Lego Worlds"],
        "resposta": "Minecraft",
        "explicacao": "Minecraft ultrapassou a marca de 300 milhões de cópias vendidas em várias plataformas."
    },
    {
        "id": 33,
        "categoria": "🎮 Games & Pop",
        "pergunta": "Qual Pokémon elétrico amarelo é o mascote oficial e mais famoso da franquia?",
        "opcoes": ["Raichu", "Pikachu", "Eevee", "Charmander"],
        "resposta": "Pikachu",
        "explicacao": "Pikachu é o fiel parceiro de Ash Ketchum e o ícone global da marca Pokémon."
    },
    {
        "id": 34,
        "categoria": "🎮 Games & Pop",
        "pergunta": "Qual jogo de batalha real popularizou a dança 'Floss' e construções rápidas?",
        "opcoes": ["PUBG", "Fortnite", "Apex Legends", "Call of Duty: Warzone"],
        "resposta": "Fortnite",
        "explicacao": "Fortnite, desenvolvido pela Epic Games, virou um fenômeno cultural global."
    },
    {
        "id": 35,
        "categoria": "🎮 Games & Pop",
        "pergunta": "No universo de O Senhor dos Anéis, quem deve destruir o Um Anel na Montanha da Perdição?",
        "opcoes": ["Frodo Bolseiro", "Aragorn", "Gandalf", "Legolas"],
        "resposta": "Frodo Bolseiro",
        "explicacao": "Frodo é o portador do Anel incumbido de levá-lo até a Montanha da Perdição em Mordor."
    },
    {
        "id": 36,
        "categoria": "🎮 Games & Pop",
        "pergunta": "Qual é a moeda fictícia do universo de 'The Legend of Zelda'?",
        "opcoes": ["Gils", "Rúpias", "Moedas de Ouro", "Esmeraldas"],
        "resposta": "Rúpias",
        "explicacao": "Link coleta rúpias coloridas (Rupees) de diferentes valores em Hyrule."
    }
]

def get_questions_by_category(category: str, limit: int = 10, seed: int = None) -> list:
    """Retorna perguntas filtradas por categoria e embaralhadas."""
    if category == "Todas as Categorias" or not category:
        pool = list(ALL_QUESTIONS)
    else:
        pool = [q for q in ALL_QUESTIONS if q["categoria"] == category]
    
    rng = random.Random(seed)
    rng.shuffle(pool)
    
    selected = pool[:min(limit, len(pool))]
    
    # Embaralhar as opções de cada pergunta para evitar padrões
    result = []
    for q in selected:
        q_copy = dict(q)
        shuffled_options = list(q["opcoes"])
        rng.shuffle(shuffled_options)
        q_copy["opcoes"] = shuffled_options
        result.append(q_copy)
        
    return result
