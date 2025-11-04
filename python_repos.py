import plotly.express as px
from requests.exceptions import ConnectionError
import requests

# Cria uma chamada de API e verifica a resposta
url = "https://api.github.com/search/repositories"
url += f"?q=language:go+sort:stars+stars:>{10_000}"

headers = {"Accept": "application/vnd.github.v3+json"}
try:
    r = requests.get(url, headers=headers)
except ConnectionError:
    print("Erro de conexão!!")
else:
    print(f"Código de status: {r.status_code}")

    # Processa os resultados gerais
    response_dict = r.json()
    print(f"Resultados completos: {not response_dict['incomplete_results']}")

    # Processa as informações do repositório
    repo_dicts = response_dict['items']
    repo_links, stars, hover_texts = [], [], []
    for repo_dict in repo_dicts:
        # Transforma os nomes dos repositórios em links ativos
        repo_name = repo_dict['name']
        repo_url = repo_dict['html_url']
        repo_links.append(f"<a href='{repo_url}'>{repo_name}<a/>")
        stars.append(repo_dict['stargazers_count'])

        # Cria textos flutuantes
        owner = repo_dict['owner']['login']
        description = repo_dict['description']
        hover_text = f"{owner}<br />{description}"
        hover_texts.append(hover_text)

    # Cria a visualização
    title = "Projetos Python mais curtidos no GitHub"
    labels = {'x': 'Repositório', 'y': 'Estrelas'}
    fig = px.bar(x=repo_links, y=stars, title=title, labels=labels,
                 hover_name=hover_texts)

    fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
                      yaxis_title_font_size=20)

    fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)
    fig.show()
