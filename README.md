# U.S. Data Science Employment Landscape 

This project aims to allow readers to get an understanding of summary statistics regarding the H-1B visa, such as number of applications, selection rate and demographic of applicants. 

## Deployment
https://gregarious-axolotl-42575b.netlify.app/

## Narrative genre and structure
The narrative genre employed is most similar to a mix of comic strip and interactive slide show due to the still text elements within multiple frames and scrolly component with animated graphs. The visual structue is mainly single frame interactivity where graphs within a window changes as user scrolls through the narrative on the left. The user can also interact wiht the grpah by hovering over it 

## linegraph 
The two line graphs outlines the annual visa cap, annual registrations and lottery selection rate over-time. Hovering over the graph will show a tooltip that has detailed numbers and explanation of 2024 anomaly for registration numbers. 

## Barcharts

The barcharts outline the country of applicants and occupations. 
If given more time, a drop down could also be implemented an additional education background variable. It would also be nice to include female and male age distributions. A animated transition between the two bar charts could also be implemented. 

## Disadvantages section 
The final section outlines the disadvantages of holding the visa, where an overlay appears in front of the text box and disappears upon hover to reveal the list of cons. 


```js
// store.js
// An extremely simple external store
import { writable } from 'svelte/store'
export default writable(0)
```
