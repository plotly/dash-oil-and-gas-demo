import os
import dash
import dash_snapshots
import redis


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
)

app.title = "Chris' Dino Dashboard"
#os.environ["REDIS_URL"] = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

snap = dash_snapshots.DashSnapshots(app)

celery_instance = snap.celery_instance
# redis_instance = redis.StrictRedis.from_url(
#     os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"), decode_responses=True
# )
REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")