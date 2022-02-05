# dtele-bot

A discord bot that helps you share your favorite movies and games with your friends.

## Commands

### Steam

- **steam**

    Sends the top search result from steam as an embed.

    ```
    Parameters: region (unspaced), search_term

    Example: steamus edith finch
    ```

    ![steam](https://raw.githubusercontent.com/dtele/dtele-bot/main/screenies/steam.png)

- **fsteam**

    Sends the top search result from steam as an embed, but you can use filters with it.

    ```
    Parameters: region (unspaced), search_term, discounted, tags, types, player_number, supported_os, supported_languages

    Example: fsteamar tags=[4x, strategy];discounted=True;player_number=co-op
    ```
    
    ![fsteam](https://raw.githubusercontent.com/dtele/dtele-bot/main/screenies/fsteam.png)

- **filterhelp**
    
    Sends the possible arguments for each parameter usable with fsteam.

    ```
    Parameters: parameter_name

    Example: filterhelp tags
    ```
    
    ![filterhelp](https://raw.githubusercontent.com/dtele/dtele-bot/main/screenies/filterhelp.png)

### TMDb

- **tmdb**

    Sends the top search result from tmdb as an embed.

    ```
    Parameters: search_term

    Example: tmdb killer sofa
    ```
    
    ![tmdb](https://raw.githubusercontent.com/dtele/dtele-bot/main/screenies/tmdb.png)
