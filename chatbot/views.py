from django.http import JsonResponse
import json

def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        
        # Lógica de respuesta del chatbot
        message_lower = message.lower()
        
        if 'hola' in message_lower or 'saludos' in message_lower:
            response_message = "¡Hola! Bienvenido al sistema de prácticas pre-profesionales. ¿En qué puedo ayudarte?"
        elif 'prácticas' in message_lower or 'practicas' in message_lower:
            response_message = "Puedes ver las prácticas disponibles en la sección 'Prácticas'. ¿Te gustaría que te redirija?"
        elif 'empresas' in message_lower:
            response_message = "Puedes encontrar la lista de empresas colaboradoras en la sección 'Empresas'."
        elif 'registro' in message_lower or 'registrarme' in message_lower:
            response_message = "Puedes registrarte como estudiante o empresa en la sección 'Registrarse' en la parte superior derecha."
        elif 'ayuda' in message_lower or 'soporte' in message_lower:
            response_message = "Estoy aquí para ayudarte. Por favor, describe tu problema o pregunta con más detalle."
        elif 'adiós' in message_lower or 'gracias' in message_lower:
            response_message = "¡De nada! Si tienes más preguntas, no dudes en consultarme. ¡Que tengas un buen día!"
        else:
            response_message = "Lo siento, no he entendido tu pregunta. ¿Podrías reformularla? Puedo ayudarte con información sobre prácticas, empresas y el proceso de registro."

        return JsonResponse({'response': response_message})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
