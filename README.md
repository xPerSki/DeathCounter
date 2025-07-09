# Death Counter (with native support for `Lies of P`)
## Usage
You can simply bind inc/dec actions to keys of your choice.  
Auto-detect feature will automatically detect if you are dead using `death_screen.png`.  
It may use ~4% of your CPU, but you can lower it by setting higher interval in `settings.json` (not recommended).
## Changing death screen
If you want to manually set the death screen for other games, you can do it by changing `death_screen.png` in the `stuff/settings.json`.  
Keep in mind that the image should be in your native resolution e.g. 1920x1080.
## Death Sound Effect
You can set a custom sound effect that will be played when you die.  
To do so, place your sound file in the `stuff` folder and set the `death_sound_effect` field in `settings.json` to the name of your sound file (e.g. `death_sound.wav`).  
You can also set it to `null` to disable the sound effect.  
## Troubleshooting
If you have any issues with the death counter, try launching it with administrator privileges.  
If it still doesn't work, you can report the issue and describe your problem in detail.
