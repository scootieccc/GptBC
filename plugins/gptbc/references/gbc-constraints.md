# GptBC — GB Studio / GBC constraints reference

Sources:
- https://www.gbstudio.dev/docs/settings/
- https://www.gbstudio.dev/docs/assets/backgrounds/
- https://www.gbstudio.dev/docs/assets/sprites/
- https://www.gbstudio.dev/docs/assets/palettes/
- https://www.gbstudio.dev/docs/project-editor/scenes/color/
- https://www.gbstudio.dev/docs/extending-gbstudio/plugins/
- https://github.com/gb-studio-dev/gb-studio-plugins

## GBC-first defaults

- Native screen: 160x144 px.
- Background dimensions: multiples of 8 px; minimum 160x144.
- Background maximum dimension: 2040 px each.
- Background maximum area: 1,048,320 px.
- Color Only background tile budget: up to 384 unique 8x8 tiles per scene.
- Monochrome / Color+Monochrome typical background tile budget: 192 unique tiles.
- Color modes expose up to 8 default background palettes and 8 sprite palettes.
- Automatic-palette backgrounds: each 8x8 tile may use at most 4 colors.
- Automatic-palette scenes: at most 8 unique 4-color palettes; using more than 7 can collide with palette 8 used by dialogue/menu UI.
- Color Only can use automatic tile flipping to reduce tile memory.
- Manual background source colors:
  #071821 #306850 #86c06c #e0f8cf
- Sprite source colors:
  #071821 #86c06c #e0f8cf #65ff00 (transparent key)
- Sprite source art should not use #306850.

## Plugin types

Official GB Studio plugin repository types include:
- assetPack
- eventsPlugin
- enginePlugin
- theme
- lang
- template

Engine plugins can replace engine files and should receive stronger conflict scrutiny.
