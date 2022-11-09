from classes.functions.functions import list_blobs

bucket = "audio_tracks_w207_final_project"

blobs = list_blobs(bucket_name=bucket, project="tokyo-epoch-367102")

print(blobs[0:10])
# print(type(blobs), type(blobs[0]))