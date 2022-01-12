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

    ![steam](https://github.com/dtele/dtele-bot/blob/add_images/screenies/steam.png?raw=true)

- **fsteam**

    Sends the top search result from steam as an embed, but you can use filters with it.

    ```
    Parameters: region (unspaced), search_term, discounted, tags, types, player_number, supported_os, supported_languages

    Example: fsteamar tags=[4x, strategy];discounted=True;player_number=co-op
    ```
    
    ![fsteam](https://github.com/dtele/dtele-bot/blob/add_images/screenies/fsteam.png?raw=true)

- **filterhelp**
    
    Sends the possible arguments for each parameter usable with fsteam.

    ```
    Parameters: parameter_name

    Example: filterhelp tags
    ```
    
    ![filterhelp](https://github.com/dtele/dtele-bot/blob/add_images/screenies/filterhelp.png?raw=true)

### TMDb

- **tmdb**

    Sends the top search result from tmdb as a search result.

    ```
    Parameters: search_term

    Example: tmdb killer sofa
    ```
    
    ![tmdb](https://github.com/dtele/dtele-bot/blob/add_images/screenies/tmdb.png?raw=true)
