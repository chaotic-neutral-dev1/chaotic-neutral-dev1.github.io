import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(title="Chaos Contained Backend Engine")


# Model danych pilnujący, aby każde zadanie miało przewidywalną strukturę
class TodoItem(BaseModel):
    file_name: str
    task: str
    char_count: int


@app.get("/api/moje_zadania", response_model=List[TodoItem])
def get_obsidian_todos():
    # Ścieżka dopasowana wprost do Twojej struktury katalogów
    obsidian_path = "./obsidian_vault/chaos-contained-vault" 
    
    todo_list = []
   
    

    
    # Jeśli folder notatek fizycznie istnieje, skanujemy pliki .md
    if os.path.exists(obsidian_path):
        for root, dirs, files in os.walk(obsidian_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            # Przechwytujemy linie zawierające marker zadania
                            
                            if "#todo" in line.lower():
                            # Czyszczenie ze składni Markdown
                                clean_task = line.replace("- [ ]", "").replace("#todo", "").replace("#TODO", "").strip()
                                todo_list.append(TodoItem(file_name=file, task=clean_task, char_count=len(clean_task)))
                           
                                                        
    return todo_list