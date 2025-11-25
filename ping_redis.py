import redis

try:
    # Connect to Redis (localhost:6379)
    r = redis.Redis(host='localhost', port=6379, db=0)

     # Ping server
    response = r.ping()
    if response:
        print("✅ Redis OK!")
    else:
        print("❌ Not Redis.")

except redis.ConnectionError as e:
    print(f"❌ Error connection: {e}")
    