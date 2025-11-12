# Importando elementos
from agent_models.google_model_shortMemory import agent_google_shortMemory
from helpers.uuid import generatorUUID

def main():
    
    agent_google_shortMemory( input="Texto", thread_id=generatorUUID() )

if __name__ == "__main__":
    main()
