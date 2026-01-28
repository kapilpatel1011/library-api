from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


app = FastAPI(
    title="Library Inventory System",
    description="In-memory API to manage book records.",
    version="1.0.0"
)

book_inventory = []

class Book(BaseModel):
    id: int = Field(..., example=101)
    title: str = Field(..., example="Atomic Habits")
    author: str = Field(..., example="James clear")
    year: int = Field(..., example=2018)

@app.post("/books", status_code=201)
def create_book(book: Book):

    for existing_book in book_inventory:
        if existing_book.id == book.id:
            raise HTTPException(status_code=400, detail=f"Book with ID {book.id} already exists.")
    
    book_inventory.append(book)
    return {"message": "Book added successfully", "data": book}

@app.get("/books/search")
def search_books_by_year(year: int = Query(..., description="Filter books by publication year")):
   
    results = [book for book in book_inventory if book.year == year]
    
    return {
        "count": len(results),
        "results": results
    }

@app.get("/books/{book_id}")
def get_book_details(book_id: int):
    """
    Fetch a single book by its ID.
    """
    for book in book_inventory:
        if book.id == book_id:
            return book
            
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def remove_book(book_id: int):
    for i, book in enumerate(book_inventory):
        if book.id == book_id:
            del book_inventory[i]
            return {"message": f"Book {book_id} has been removed."}
            
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/")
def root():
    return {"status": "running", "docs_url": "/docs"}