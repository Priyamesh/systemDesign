"""
- You are building instagram reels where users can upload and delete reels/videos.
- Each `reel`  is a **string** of digits, where the `ith` digit of the string represents the content of the reel at minute `i`. For example, the first digit represents the content at minute `0` in the reel, the second digit represents the content at minute `1` in the reel, and so on. Viewers of reels can also like and dislike reels.
- Internally, the platform keeps track of the **number of views, likes, and dislikes** on each reel.
- Implement functionality for a `ReelPlatform` class including but not limited to:
    - upload(str reel) → return the ID of the reel
    - remove(videoID) → return bool if removal works
    - watch(videoID, startMinute, endMinute) → str
    - like(videoID) → None
    - dislike(videoID) → None
    - getLikesAndDislikes(videoID) → dict of likes and dislikes
    - getViews(videoID) → int
"""

import uuid

class Reel:
    
    def __init__(self, content):
       self.content = content
       self.like = 0
       self.dislike = 0
       self.views = 0
       self.id = uuid.uuid4()

    def getReelContent(self, startMinute, endMinute):
        return self.content[startMinute:endMinute]

    def viewReel(self):
        self.views += 1

    def getViews(self):
        return self.views
    
    def likeReel(self):
        self.like += 1

    def dislikeReel(self):
        self.dislike += 1

    def getLikeDislike(self):
        return {
            'like':self.like,
            'dislike':self.dislike
        }

class ReelPlatform:
    def __init__(self):
        self.reels = {}

    def _getReel(self, id):
        return self.reels.get(id,None)

    def upload(self, content):
        reel = Reel(content)
        self.reels[reel.id] = reel
        return reel.id

    def remove(self, id):
        if id in self.reels:
            del self.reels[id]
            return True
        return False

    def watch(self, id, startMinute, endMinute):
        reel = self._getReel(id)
        if reel:
            reel.viewReel()
            return reel.getReelContent(startMinute, endMinute)
        else:
            return f"No reel found for id {id}"
        
    def like(self, id):
        reel = self._getReel(id)
        if reel:
            reel.likeReel()
            print("Liked!")
        else:
            return f"No reel found for id {id}"
        
    def dislike(self, id):
        reel = self._getReel(id)
        if reel:
            reel.dislikeReel()
            print("Disliked")
        else:
            return f"No reel found for id {id}"

    def getLikesAndDislikes(self, id):
        reel = self._getReel(id)
        if reel:
            return reel.getLikeDislike()
        else:
            return f"No reel found for id {id}"


    def getViews(self, id):
        reel = self._getReel(id)
        if reel:
            viewCount = reel.getViews()
            return viewCount
        else:
            return f"No reel found for id {id}"
        
        
        
        
        
        

    
    
        
insta = ReelPlatform()
content1 = insta.upload("somecontentintextformat")
print(content1)

print(insta.watch(content1, 4, 16))
print(insta.getViews(content1))
print(insta.getLikesAndDislikes(content1))
print(insta.like(content1))
print(insta.getLikesAndDislikes(content1))

    