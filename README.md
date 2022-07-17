# <img src="https://user-images.githubusercontent.com/73225256/179392008-0e45f754-e79a-4a9f-a875-2006eb1257dc.png" width='40px'> Tripari's Back-end

### **Back-end for [Triparis.work](https://triparis.work), built with FastAPI/SQLAlchemy**

### Click here for [live demo](https://triparis.work/api/v1/docs)
![image](https://user-images.githubusercontent.com/73225256/179392332-03a73c63-130a-49dc-b1a0-7411c7c407a2.png)


## Description
- A project assists travelers in planning their upcoming trips, storing noteworthy aspects of their experiences, and sharing them with other travelers.

## Features
- Authenticate with OAuth2 + JWT token
- Validate whether the registered email exists in reality to avoid spamming
- CRUD operations for travelers's trips
- CRUD operations for locations that travelers may visit during the trip
- CRUD operations for checklist that travelers may need to carry for the trip
- Like/Unlike trip posts, comments
- Comment/Reply Comment trip posts
- Reset password via email
- Remind user about their upcoming trip via email before the trip start 1 day
- Test API directly with an interactive API document (SwaggerUI)
- Store files on Azure Blob Storage

## Tech stack
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL**
- **Celery**