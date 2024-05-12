'-------------------------------------------------------------------------------------------------------------------------------------------'
#                                                       IMPORT DEPENDENCIES 
from typing_extensions import Unpack
from fastapi import FastAPI, HTTPException, Form
from pymongo import MongoClient
from pydantic import BaseModel, ConfigDict
from bson import ObjectId
from typing import Annotated
from collections import defaultdict
from  datetime import datetime
from fastapi.encoders import jsonable_encoder

app = FastAPI()

'-------------------------------------------------------------------------------------------------------------------------------------------'
#                                                           MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["harry"]
d=defaultdict(str)
d1=defaultdict(str)

'------------------------------------------------------------------------------------------------------------------------------------------'
#                                                                Data model
class Post(BaseModel):
    title: str
    content: str

class Comments(BaseModel):
    content:str
    timestamp:datetime

class Reaction(BaseModel):
    like:int
    dislike:int

'------------------------------------------------------------------------------------------------------------------------------------------'
#                                                               MongoDB collection
posts_collection = db["posts"]
comment_collection = db["comments"]
reaction_collection=db["reactions"]

'------------------------------------------------------------------------------------------------------------------------------------------'
#                                                           CRUD operations for posts
class PostDB:
    @staticmethod
    def create_post(post_data: str):
        post_id = posts_collection.insert_one(post_data).inserted_id
        return str(post_id)

    @staticmethod
    def get_post(post_id: str):
        response = posts_collection.find_one({"_id": ObjectId(post_id)})
        response['id'] = str(response['_id'])
        del[response['_id']]
        try:
            if response:
                return {
                    'Title':response['title'],
                    'Content':response['content']

                }
            else:
                raise HTTPException(status_code=404, detail="Post not found")
        except:
            print('Error')

    @staticmethod
    def update_post(post_id:str, post_data:str):
        posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_data})

    @staticmethod
    def delete_post(post_id:str):
        posts_collection.delete_one({"_id": ObjectId(post_id)})


'------------------------------------------------------------------------------------------------------------------------------------------'
#                                                           CRUD operations for Comments
class CommentsDB:
    @staticmethod
    def create_comment(comment_data: str,post_id:str):
        Post_id = posts_collection.find_one({"_id": ObjectId(post_id)})
        Post_id['id'] = str(Post_id['_id'])
        del[Post_id['_id']]
        comment_id = comment_collection.insert_one(comment_data).inserted_id
        d[Post_id['id']]=comment_id
        return str(d[Post_id['id']])
    
    @staticmethod
    def get_comment_with_ID(comment_id: str):
        response = comment_collection.find_one({"_id": ObjectId(comment_id)})
        response['id'] = str(response['_id'])
        del[response['_id']]
        try:
            if response:
                return response
            else:
                raise HTTPException(status_code=404, detail="Comment not found")
        except:
            print('Error')

    
    
    @staticmethod
    def update_comment(post_id:str, post_data:str):
        comment_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_data})

    @staticmethod
    def delete_comment(post_id:str):
        comment_collection.delete_one({"_id": ObjectId(post_id)})


'------------------------------------------------------------------------------------------------------------------------------------------'
#                                                 CRUD operations for Reaction(like/dislike)
class ReactionDB:
    def reaction_on_comment(comment_id:str,reaction_data:int):
        print('YES')
        comment_id = comment_collection.find_one({"_id": ObjectId(comment_id)})
        comment_id['id'] = str(comment_id['_id'])
        del[comment_id['_id']]
        x=reaction_collection.insert_one(reaction_data).inserted_id
        d1[comment_id['id']]=x
        return str(d1[comment_id['id']])

    def reaction_on_post(post_id:str,reaction_data:int):
        print(post_id)
        Post_id = posts_collection.find_one({"_id": ObjectId(post_id)})
        Post_id['id'] = str(Post_id['_id'])
        del[Post_id['_id']]
        x=reaction_collection.insert_one(reaction_data).inserted_id
        d1[Post_id['id']]=x
        return str(d1[Post_id['id']])
    
    
'-------------------------------------------------------------------------------------------------------------------------------------------'
#                                                   API endpoint for CRUD operations in post

#post bloging post
@app.post("/posts/")
def create_post(post: Post):
    """
    write posts
    """
    post_id = PostDB.create_post(post.__dict__)
    return {"post_id": post_id}


# read post
@app.get("/posts/{post_id}")
def get_post_with_id(post_id):
    """
    read posts
    """
    post=PostDB.get_post(post_id)
    return post

# delete post
@app.delete("/posts/{post_id}")
def del_post(post_id):
    """
    delete posts
    """
    post_id = PostDB.delete_post(post_id)
    return {"post deleted":post_id}


# update post
@app.put("/posts/{post_id}")
def update_post(post_id:str,post_data:Post):
    """
    Update/edit posts
    """
    post=PostDB.update_post(post_id, post_data.__dict__)
    return post

'------------------------------------------------------------------------------------------------------------------------------------------'
#                                               API endpoint for CRUD operations in comment
@app.post("/comments/{post_id}")
def create_comment(comment_data:Comments,post_id:str):
    """
    write comments
    """
    json_compatible_item_data = jsonable_encoder(comment_data)
    com=CommentsDB.create_comment(json_compatible_item_data,post_id)
    return {"commentID":com}

# read comments
@app.get("/comments/{comment_id}")
def get_comment_with_id(comment_id):
    """
    read comments
    """
    com=CommentsDB.get_comment_with_ID(comment_id)
    return com

# delete comments
@app.delete("/comments/{comment_id}")
def del_comment(comment_id):
    """
    delete comments
    """
    comment_id = CommentsDB.delete_comment(comment_id)
    return {"comment deleted":comment_id}


# update comments
@app.put("/comments/{comment_id}")
def update_comment(comment_id:str,comment_data:Comments):
    """
    Update/edit comments
    """
    post=CommentsDB.update_comment(comment_id, comment_data.__dict__)
    return post
'-----------------------------------------------------------------------------------------------------------------------------------------'
#                                               API endpoint for CRUD operations in reaction

@app.post("/commentlike/{comment_id}")
def like_COMMENT(comment_id:str,reaction_data:Reaction):
    """
    Get the like/dislike for a comment
    """
    y=ReactionDB.reaction_on_comment(comment_id,reaction_data.__dict__)
    return {"Like_comment_ID":y}

#like post
@app.post("/postlike/{post_id}")
def like_POST(post_id:str,reaction_data:Reaction):
    """
    Get the like/dislike for a post
    """
    rec=ReactionDB.reaction_on_post(post_id,reaction_data.__dict__)
    return {"Like_post_ID":rec}
