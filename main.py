from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")


#-----------------------------------------#
#------- Declaramos los datasets ---------#
#-----------------------------------------#
endpoint_user_data = pd.read_csv('./dataset/Endpoints/endpoint_userdata.csv')
endpoint_countreviews = pd.read_csv('./dataset/Endpoints/endpoint_countreviews.csv')
endpoint_genre = pd.read_csv('./dataset/Endpoints/endpoint_genre.csv')
endpoint_userforgenre = pd.read_csv('./dataset/Endpoints/endpoint_userforgenre.csv')
endpoint_developer = pd.read_csv('./dataset/Endpoints/endpoint_developer.csv')
endpoint_sentiment_analysis = pd.read_csv('./dataset/Endpoints/endpoint_sentiment_analysis.csv')


#---- Home ----#
@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_adress = ('./static/html/index.html')
    return FileResponse(html_adress, status_code= 200)



#---- Funcion 1 ----#
@app.get('/function1')
async def userdata(parametro: str):
    df = endpoint_user_data.loc[endpoint_user_data['user_id'] == parametro]
    
    if not df.empty:
        user = df['user_id'].values[0]
        spent = df['total_spent'].values[0]
        percent_recommend = df['percent_recommend'].values[0]
        item_count = df['items_count'].values[0]

        
        return f'El usuario {user} gastó ${spent}, tiene {item_count} items el cual recomendó un {percent_recommend}% '
    else:
        return f'No hay registros de ese usuario'


#---- Funcion 2 ----#
@app.get('/function2')
async def countreviews(desde:str, hasta:str):
    
    df = endpoint_countreviews[(endpoint_countreviews['posted'] >= desde) & (endpoint_countreviews['posted'] <= hasta)]

    if not df.empty:
        user_count = df['user_id'].nunique()
        recommend_count = df['recommend'].count()
        recommend_sum = df['recommend'].sum()
        recommend_percent = round(recommend_sum / recommend_count * 100, 2)
        return f'Desde {desde} hasta {hasta} , {user_count} usuarios realizaron reviews, el cual solo el {recommend_percent}% de usuarios recomendaron juegos'
    else:
        return 'No hay registros entre esas fechas'


#---- Funcion 3 ----#
@app.get('/function3')
async def genre(genero: str):
    df = endpoint_genre[endpoint_genre['genres'] == genero]
    
    if not df.empty:
        genre = df.iloc[0, 0]
        ranking = df.iloc[0, 2]
        return f'El género {genre} se encuentra en el puesto número {ranking} del ranking'
    else:
        return 'No se encuentran registros de ese género'
    
    
#---- Funcion 4 ----#
@app.get('/function4')
async def userforgenre(genero: str):
    if genero in endpoint_userforgenre['genres'].unique():
        df = endpoint_userforgenre[endpoint_userforgenre['genres'] == genero]

        ranking = [f'Puesto Nro {i + 1}' for i in range(len(df))]

        users_info = [
            f'Usuario: {user_id}  ||  URL del usuario: {url_user}'
            for user_id, url_user in zip(df['user_id'], df['user_url'])
        ]

        return dict(zip(ranking, users_info))
    else:
        return 'No hay registros con ese género'
    

#---- Funcion 5 ----#
@app.get('/function5')
async def developer(desarrollador: str):
    if desarrollador in endpoint_developer['developer'].unique():
        df = endpoint_developer[endpoint_developer['developer'] == desarrollador]

        mi_dict = {
            year: f'Cantidad de Items: {items_count}  ||  Contenido FREE: {free_percent:}%'
            for year, items_count, free_percent in zip(df['year'], df['items_count'], df['free_percentage'])
        }

        return mi_dict
    else:
       
        return {}


#---- Funcion 6 ----#
@app.get('/function6')
async def sentiment_analysis(parametro: int):

    if parametro in endpoint_sentiment_analysis['year_posted'].unique():
        df = endpoint_sentiment_analysis[endpoint_sentiment_analysis['year_posted'] == parametro]

        sentiment_counts = df['sentiment_analysis'].value_counts().to_dict()

        resultado= {
            'Negativo': sentiment_counts.get(0, 0),
            'Neutral': sentiment_counts.get(1, 0),
            'Positivo': sentiment_counts.get(2, 0)
        }
        return f'La cantidad de resenias que hubo en el anio {parametro} es:  {resultado}'
    else:
        resultado= f'No hay registros con ese año'
        return resultado
    

    
