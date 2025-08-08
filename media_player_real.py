from pywinauto import Desktop, Application
from pywinauto.application import ProcessNotFoundError
from pypresence import Presence
import time

def get_media_info():
    try:
        desktop = Desktop(backend="uia") # New apps. If legacy, use win32.
        window = desktop.window(title_re="Media Player")
    except ProcessNotFoundError:
        print("Media Player getting milk.")
        return None
    
    # Printing all elements in Media Player
    texts = window.descendants(control_type="Text")
    for t in texts:
        print(f"Text found: {t.window_text()}")
        
    # Skip words will remove the common words listed in media player. Especially with the 2 words. 
    # Please don't go to the music library: I do not know how to force it focus on the 
    # bottom quadrant of the tab, so it's adding the stuff in the middle.
    skip_words = {"home", "recent media", "play", "pause", "next", "time elapsed",
                  "recent media","time remaining", "media player", 
                  "add folder", "shuffle and play", "sort by:",
                  "a - z", "all genres"}

    title = next(
        (t.window_text() for t in texts
         if len(t.window_text().split())>=2
         and t.window_text().strip().lower() not in skip_words
         )
         ,None
    )

    artist = None
    if title:
        try:
            for t in texts:
                text_content = t.window_text().strip()
                if text_content and text_content.lower() not in skip_words and text_content != title:
                    artist = text_content
        except (StopIteration, IndexError):
            artist = None
            print("Error occured while trying to find artist (author probably didn't find the exception for that :3).")

    return {
        "title": title or "Unknown Title",
         "artist": artist or "Unknown Artist"
    }

info = get_media_info()
print(info)
print(f"Title: {info['title']}")
print(f"Artist: {info['artist']}")

def run_rich_presence(client_id):

    RPC = Presence(client_id)
    RPC.connect()
    print("Discord RPC connected.")

    while True:
        info = get_media_info()
        if info:
            print(f"Updating Discord: {info['artist']} — {info['title']}")
            RPC.update(
                details=f"🎵 {info['title']}",
                state=f"👤 {info['artist']}",
                large_image="media_icon",
                large_text="Windows 11 Media Player",
                start=time.time()
            )
        else:
            print("Media info unavailable — clearing RPC.")
            try:
                RPC.clear()
            except Exception:
                pass
        time.sleep(10)

if __name__ == "__main__":
    YOUR_CLIENT_ID = "1403044786986029067"
    run_rich_presence(YOUR_CLIENT_ID)