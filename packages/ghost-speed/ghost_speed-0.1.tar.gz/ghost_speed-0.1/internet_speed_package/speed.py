# internet_speed_package/speed.py

import speedtest

def get_internet_speed():
    """Returns the download and upload speeds in Mbps."""
    st = speedtest.Speedtest()
    st.get_best_server()  # Find the best server based on ping
    
    # Get download and upload speeds (in bits per second)
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    
    return download_speed, upload_speed
