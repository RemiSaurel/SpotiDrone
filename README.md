# SpotiDrone

This application looks on your currently most listened songs and create a playlist of recommendations about one of the songs picked randomly.\
The popularity is set to minimum value so you can discover new upcoming bangers 😇

## How to test it ?
- Make sure to create a `.env` file with your credentials (see the `.env.example` file)
- Install the requirements with:
```
pip install -r requirements.txt
```
- Execute with the number of songs you want on your playlist (50 is max due to Spotify API recent tracks):
```
python3 main.py -n NUMBER_OF_SONGS
``` 

## Example
![CleanShot 2023-03-22 at 23 32 48](https://user-images.githubusercontent.com/50367862/227053269-c68a901a-c61e-47b2-bfd5-ebf7f80627ba.png)
