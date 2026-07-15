"""
Semeadura do catálogo de EXERCÍCIOS PERSONALIZADOS (Treino Personalizado).

Cria um Training por (categoria, nível), nomeado "<CATEGORIA> - <NÍVEL>", e
vincula os exercícios na ordem. Reaproveita os modelos Exercise/Training/
TrainingExercise (mesmo padrão de seed_banco.py).

Idempotente: usa get_or_create para Exercise/Training e recria os vínculos
(TrainingExercise) de cada treino a cada execução. NÃO apaga Mãos/Pés.

Ordem recomendada de execução:
    python manage.py migrate
    python seed_banco.py            # popula Mãos/Pés/relaxamento
    python seed_personalizado.py    # popula o catálogo personalizado

Dados extraídos de "Exercícios ArtriApp.md" (seção "Treino personalizado").
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artri_app_api.settings')
django.setup()

from authentication.models import Exercise, Training, TrainingExercise

DIFF_MAP = {'INICIANTE': 'Easy', 'INTERMEDIÁRIO': 'Medium', 'AVANÇADO': 'Hard'}

# Sufixo padrão de observação para exercícios com carga.
PESO = (' Você poderá usar um peso (halter), uma garrafa cheia de água ou areia, '
        'ou qualquer outro objeto pesado.')

# Textos de instrução reutilizados.
I_10x30 = 'Faça o exercício 10 vezes. Depois, descanse 30 segundos e faça mais 10 vezes.'
I_10 = 'Faça o exercício 10 vezes.'
I_40s_1min_seq = 'Faça o exercício por 40 segundos. Depois, descanse 1 minuto e vá para o próximo exercício.'
I_1min_30s_seq = 'Faça o exercício por 1 minuto. Depois, descanse 30 segundos e vá para o próximo exercício.'
I_10x1min = 'Faça o exercício 10 vezes. Depois, descanse 1 minuto e faça mais 10 vezes.'
I_30s_1min = 'Faça o exercício ficando nessa posição por 30 segundos. Depois, descanse 1 minuto e faça mais 30 segundos.'
I_10x40s_3 = 'Faça o exercício 10 vezes. Depois, descanse 40 segundos e faça mais 10 vezes. Faça isso 3 vezes no total.'
I_30s40s_3 = 'Faça o exercício ficando nessa posição por 30 segundos. Depois, descanse 40 segundos e faça mais 30 segundos. Faça isso 3 vezes no total.'
I_1215_3 = 'Faça o exercício de 12 a 15 vezes. Depois, descanse 40 segundos e faça mais 12 a 15 vezes. Faça isso 3 vezes no total.'
I_along40 = 'Faça o exercício mantendo nessa posição por 40 segundos.'

# Cada exercício: (nome, séries/repetições, descanso, instruções, link)
CATALOG = {
    'INICIANTE': {
        'MOBILIDADE PERNAS': [
            ('Círculos com a perna', '2x10', '30s', I_10x30, 'https://youtu.be/aQ28TYdqiuU'),
            ('Círculos com o pé', '2x10', '30s', I_10x30, 'https://youtu.be/t778SVu8q7k'),
            ('Pernas para frente e para trás', '2x10', '30s', I_10x30, 'https://youtu.be/niQW5YigTR8'),
        ],
        'MOBILIDADE BRAÇOS': [
            ('Círculos com os braços', '2x10', '30s', I_10x30, 'https://youtu.be/3yB1qsEBnek'),
            ('Subir e descer os ombros', '2x10', '30s', I_10x30, 'https://youtu.be/GTnFmY5hcXo'),
            ('Círculos com os punhos', '2x10', '30s', I_10x30, 'https://youtu.be/kmtUGLHAVFM'),
        ],
        'MOBILIDADE TRONCO': [
            ('Descer e subir o tronco sentado', '2x10', '30s', I_10x30, 'https://youtu.be/_zTyUPCaCD8'),
            ('Gato arrepiado', '2x10', '30s', I_10x30, 'https://youtu.be/Nn-NbV8I3DI'),
        ],
        'AERÓBICO': [
            ('Marcha no lugar', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/u_nPrwSOZAM'),
            ('Marcha no lugar com toque no joelho', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/dj-mW5LIwns'),
            ('Polichinelo adaptado', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/n6KZuSUL6js'),
        ],
        'FORTALECIMENTO MEMBRO INFERIOR': [
            ('Sentar e levantar da cadeira', '2x10', '60s',I_10x1min, 'https://youtu.be/JJqRkKUepSk'),
            ('Subir e descer o quadril deitado', '2x10', '60s',I_10x1min, 'https://youtu.be/Nvet_zfREBo'),
            ('Subir o quadril deitado', '2x30s', '60s',I_30s_1min, 'https://youtu.be/iUweFr2eT3Y'),
            ('Ficar na ponta dos pés sentado', '2x10', '60s',I_10x1min, 'https://youtu.be/_mVxW3xlZow'),
            ('Abrir a perna em pé', '2x10', '60s',I_10x1min, 'https://youtu.be/faJzMqWw6Ko'),
        ],
        'FORTALECIMENTO MEMBRO SUPERIOR': [
            ('Elevação lateral dos braços', '2x10', '60s',I_10x1min + PESO, 'https://youtu.be/ORl5e76_Ptw'),
            ('Dobrar o cotovelo', '2x10', '60s',I_10x1min + PESO, 'https://youtu.be/uf1aQbuJvWg'),
            ('Elevação dos braços para frente', '2x10', '60s',I_10x1min + PESO, 'https://youtu.be/oc1wndKZKb0'),
            ('Rotação do braço para fora', '2x10', '60s',I_10x1min + PESO, 'https://youtu.be/g3EmpJIpiMw'),
            ('Rotação do braço para dentro', '2x10', '60s',I_10x1min + PESO, 'https://youtu.be/tQTOvA5OEbM'),
        ],
        'FORTALECIMENTO CORE': [
            ('Abdominal em pé', '2x10', '60s',I_10x1min, 'https://youtu.be/fC7Bieh5dg0'),
            ('Abdominal deitado', '2x10', '60s',I_10x1min, 'https://youtu.be/5_-nqivKzNM'),
            ('Prancha com apoio dos joelhos', '2x30s', '60s',I_30s_1min, 'https://youtu.be/3nFTZiC-r60'),
        ],
        'ALONGAMENTO': [
            ('Parte da frente da perna', '1x40s', '–', I_along40, 'https://youtu.be/J2Vq8rvkJwM'),
            ('Parte de trás da perna', '1x40s', '–', I_along40, 'https://youtu.be/eiigoyq0144'),
            ('Panturrilha', '1x40s', '–', I_along40, 'https://youtu.be/ukCxzDBg_nY'),
            ('Braços esticados acima', '1x40s', '–', I_along40, 'https://youtu.be/usIQwhKcOF4'),
            ('Braços esticados para trás', '1x40s', '–', I_along40, 'https://youtu.be/glWOhWXijtM'),
            ('Braços esticados na frente', '1x40s', '–', I_along40, 'https://youtu.be/pPQWB8n-SoU'),
            ('Glúteos', '1x40s', '–', I_along40, 'https://youtu.be/GkkI4luB1AA'),
        ],
    },
    'INTERMEDIÁRIO': {
        'MOBILIDADE PERNAS': [
            ('Círculos com a perna', '1x10', '–', I_10, 'https://youtu.be/aQ28TYdqiuU'),
            ('Círculos com o pé', '1x10', '–', I_10, 'https://youtu.be/t778SVu8q7k'),
            ('Pernas para frente e para trás', '1x10', '–', I_10, 'https://youtu.be/niQW5YigTR8'),
        ],
        'MOBILIDADE BRAÇOS': [
            ('Círculos com os braços', '1x10', '–', I_10, 'https://youtu.be/3yB1qsEBnek'),
            ('Subir e descer os ombros', '1x10', '–', I_10, 'https://youtu.be/GTnFmY5hcXo'),
            ('Círculos com os punhos', '1x10', '–', I_10, 'https://youtu.be/kmtUGLHAVFM'),
        ],
        'MOBILIDADE TRONCO': [
            ('Descer e subir o tronco em pé', '1x10', '–', I_10, ''),
            ('Gato arrepiado', '1x10', '–', I_10, 'https://youtu.be/Nn-NbV8I3DI'),
        ],
        'AERÓBICO': [
            ('Marcha no lugar', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/u_nPrwSOZAM'),
            ('Marcha no lugar com toque no joelho', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/dj-mW5LIwns'),
            ('Polichinelo adaptado', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/n6KZuSUL6js'),
            ('Polichinelo', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/yqepwCAgegM'),
            ('Corrida no lugar', '1x40s', '60s',I_40s_1min_seq, 'https://youtu.be/C7ilpg4AI1M'),
        ],
        'FORTALECIMENTO MEMBRO INFERIOR': [
            ('Sentar e levantar da cadeira', '3x10', '40s', I_10x40s_3, 'https://youtu.be/JJqRkKUepSk'),
            ('Agachamento', '3x10', '40s', I_10x40s_3, 'https://youtu.be/rjsgfMKWSxA'),
            ('Subir e descer o quadril deitado', '3x10', '40s', I_10x40s_3, 'https://youtu.be/Nvet_zfREBo'),
            ('Ficar na ponta dos pés em pé', '3x10', '40s', I_10x40s_3, 'https://youtu.be/6riWR0KY9Jg'),
            ('Abrir a perna para o lado deitado', '3x10', '40s', I_10x40s_3, 'https://youtu.be/lq46lTD8Xtc'),
        ],
        'FORTALECIMENTO MEMBRO SUPERIOR': [
            ('Elevação lateral dos braços', '3x10', '40s', I_10x40s_3 + PESO, 'https://youtu.be/ORl5e76_Ptw'),
            ('Dobrar o cotovelo', '3x10', '40s', I_10x40s_3 + PESO, 'https://youtu.be/uf1aQbuJvWg'),
            ('Elevação dos braços para frente', '3x10', '40s', I_10x40s_3 + PESO, 'https://youtu.be/oc1wndKZKb0'),
            ('Flexão de braço na parede', '3x10', '40s', I_10x40s_3, 'https://youtu.be/fgxjUmiMt1M'),
            ('Rotação do braço para fora', '3x10', '40s', I_10x40s_3 + PESO, 'https://youtu.be/g3EmpJIpiMw'),
            ('Rotação do braço para dentro', '3x10', '40s', I_10x40s_3 + PESO, 'https://youtu.be/tQTOvA5OEbM'),
        ],
        'FORTALECIMENTO CORE': [
            ('Abdominal em pé', '3x10', '40s', I_10x40s_3, 'https://youtu.be/fC7Bieh5dg0'),
            ('Abdominal deitado', '3x10', '40s', I_10x40s_3, 'https://youtu.be/5_-nqivKzNM'),
            ('Prancha com apoio dos joelhos', '3x30s', '40s', I_30s40s_3, 'https://youtu.be/3nFTZiC-r60'),
            ('Prancha', '3x30s', '40s', I_30s40s_3, 'https://youtu.be/FV-cY1Hw3Bw'),
        ],
        'ALONGAMENTO': [
            ('Parte da frente da perna', '1x40s', '–', I_along40, 'https://youtu.be/J2Vq8rvkJwM'),
            ('Parte de trás da perna', '1x40s', '–', I_along40, 'https://youtu.be/eiigoyq0144'),
            ('Panturrilha', '1x40s', '–', I_along40, 'https://youtu.be/ukCxzDBg_nY'),
            ('Glúteos', '1x40s', '–', I_along40, 'https://youtu.be/GkkI4luB1AA'),
            ('Braços esticados acima', '1x40s', '–', I_along40, 'https://youtu.be/usIQwhKcOF4'),
            ('Braços esticados para trás', '1x40s', '–', I_along40, 'https://youtu.be/glWOhWXijtM'),
            ('Braços esticados na frente', '1x40s', '–', I_along40, 'https://youtu.be/pPQWB8n-SoU'),
        ],
    },
    'AVANÇADO': {
        'MOBILIDADE PERNAS': [
            ('Círculos com a perna', '1x10', '–', I_10, 'https://youtu.be/aQ28TYdqiuU'),
            ('Círculos com o tornozelo', '1x10', '–', I_10, 'https://youtu.be/t778SVu8q7k'),
            ('Pernas para frente e para trás', '1x10', '–', I_10, 'https://youtu.be/niQW5YigTR8'),
        ],
        'MOBILIDADE BRAÇOS': [
            ('Círculos com os braços', '1x10', '–', I_10, 'https://youtu.be/3yB1qsEBnek'),
            ('Subir e descer os ombros', '1x10', '–', I_10, 'https://youtu.be/GTnFmY5hcXo'),
            ('Círculos com os punhos', '1x10', '–', I_10, 'https://youtu.be/kmtUGLHAVFM'),
        ],
        'MOBILIDADE TRONCO': [
            ('Descer e subir o tronco em pé', '1x10', '–', I_10, ''),
            ('Gato arrepiado', '1x10', '–', I_10, 'https://youtu.be/Nn-NbV8I3DI'),
        ],
        'AERÓBICO': [
            ('Marcha no lugar', '1x60s', '30s', I_1min_30s_seq, 'https://youtu.be/u_nPrwSOZAM'),
            ('Marcha no lugar com toque no joelho', '1x60s', '30s', I_1min_30s_seq, 'https://youtu.be/dj-mW5LIwns'),
            ('Polichinelo adaptado', '1x60s', '30s', I_1min_30s_seq, 'https://youtu.be/n6KZuSUL6js'),
            ('Polichinelo', '1x60s', '30s', I_1min_30s_seq, 'https://youtu.be/yqepwCAgegM'),
            ('Corrida no lugar', '1x60s', '30s', I_1min_30s_seq, 'https://youtu.be/C7ilpg4AI1M'),
        ],
        'FORTALECIMENTO MEMBRO INFERIOR': [
            ('Sentar e levantar da cadeira', '3x12', '40s', I_1215_3, 'https://youtu.be/JJqRkKUepSk'),
            ('Subir e descer o quadril deitado', '3x12', '40s', I_1215_3, 'https://youtu.be/Nvet_zfREBo'),
            ('Abrir a perna para o lado deitado', '3x12', '40s', I_1215_3, 'https://youtu.be/lq46lTD8Xtc'),
            ('Ficar na ponta dos pés em pé', '3x12', '40s', I_1215_3, 'https://youtu.be/6riWR0KY9Jg'),
            ('Agachamento', '3x12', '40s', I_1215_3, 'https://youtu.be/rjsgfMKWSxA'),
            ('Subir e descer o quadril com pé na cadeira', '3x12', '40s', I_1215_3, ''),
            ('Cadeirinha na parede', '3x30s', '40s', I_30s40s_3, ''),
        ],
        'FORTALECIMENTO MEMBRO SUPERIOR': [
            ('Elevação lateral dos braços', '3x12', '40s', I_1215_3 + PESO, 'https://youtu.be/ORl5e76_Ptw'),
            ('Dobrar o cotovelo', '3x12', '40s', I_1215_3 + PESO, 'https://youtu.be/uf1aQbuJvWg'),
            ('Elevação dos braços para frente', '3x12', '40s', I_1215_3 + PESO, 'https://youtu.be/oc1wndKZKb0'),
            ('Flexão de braço na parede', '3x12', '40s', I_1215_3, 'https://youtu.be/fgxjUmiMt1M'),
            ('Dobrar o braço atrás da cabeça', '3x12', '40s', I_1215_3 + PESO, ''),
            ('Rotação do braço para fora', '3x12', '40s', I_1215_3 + PESO, 'https://youtu.be/g3EmpJIpiMw'),
            ('Rotação do braço para dentro', '3x12', '40s', I_1215_3 + PESO, 'https://youtu.be/tQTOvA5OEbM'),
        ],
        'FORTALECIMENTO CORE': [
            ('Abdominal em pé', '3x10', '40s', I_10x40s_3, 'https://youtu.be/fC7Bieh5dg0'),
            ('Abdominal deitado', '3x10', '40s', I_10x40s_3, 'https://youtu.be/5_-nqivKzNM'),
            ('Prancha', '3x30s', '40s', I_30s40s_3, 'https://youtu.be/FV-cY1Hw3Bw'),
            ('Abdominal bicicleta', '3x10', '40s', I_10x40s_3, 'https://youtu.be/UfYKwu_7uLU'),
            ('Prancha lateral', '3x30s', '40s', I_30s40s_3, ''),
        ],
        'ALONGAMENTO': [
            ('Parte da frente da perna', '1x40s', '–', I_along40, 'https://youtu.be/J2Vq8rvkJwM'),
            ('Parte de trás da perna', '1x40s', '–', I_along40, 'https://youtu.be/eiigoyq0144'),
            ('Panturrilha', '1x40s', '–', I_along40, 'https://youtu.be/ukCxzDBg_nY'),
            ('Glúteos', '1x40s', '–', I_along40, 'https://youtu.be/GkkI4luB1AA'),
            ('Braços esticados para cima', '1x40s', '–', I_along40, 'https://youtu.be/usIQwhKcOF4'),
            ('Braços esticados para trás', '1x40s', '–', I_along40, 'https://youtu.be/glWOhWXijtM'),
            ('Braços esticados na frente', '1x40s', '–', I_along40, 'https://youtu.be/pPQWB8n-SoU'),
        ],
    },
}


def seed():
    print('📖 Semeando catálogo de Exercícios Personalizados...')
    total_treinos = 0
    total_vinculos = 0

    for level, groups in CATALOG.items():
        db_diff = DIFF_MAP[level]
        for base, exercises in groups.items():
            training_name = f'{base} - {level}'

            training, _ = Training.objects.get_or_create(
                name=training_name,
                defaults={
                    'difficulty': db_diff,
                    'description': f'Exercícios de {base.title()} ({level.title()}).',
                },
            )
            # Garante a dificuldade correta mesmo se o treino já existir.
            if training.difficulty != db_diff:
                training.difficulty = db_diff
                training.save()

            # Recria os vínculos para manter a ordem e ser idempotente.
            TrainingExercise.objects.filter(training=training).delete()

            for order, (name, sets, rest, desc, link) in enumerate(exercises):
                exercise, _ = Exercise.objects.get_or_create(
                    name=name,
                    difficulty=db_diff,
                    defaults={
                        'sets_reps': sets,
                        'rest_time': rest,
                        'description': desc,
                        'tutorial_link': link,
                    },
                )
                TrainingExercise.objects.create(
                    training=training,
                    exercise=exercise,
                    order=order,
                )
                total_vinculos += 1

            total_treinos += 1
            print(f'   - {training_name}: {len(exercises)} exercícios.')

    print(f'\n🎉 Concluído! {total_treinos} treinos personalizados, '
          f'{total_vinculos} vínculos de exercícios.')


if __name__ == '__main__':
    seed()
