# A talk about my pet project "zef"

The talk is a slides presentation that can be navigated through via a "timeline" diagram.

## Slides
- based on revealJS

## Timeline

- timeline is in Mermaid file [timeline.mmd](./timeline.mmd)
- converted into svg via script [script/build-svg.sh](./script/build-svg.sh)
- then **sozi** is used to "animate" the svg resulting in html file [timeline-presentation](./timeline-presentation)

## Gluing the two together

- the main page has 2 frames:
  - the slides
  - the timeline
- slides have ids and timeline frames have ids too
- when the timeline animation enters a frame, the corresponding slide is shown
- reciprocally, when a slide with id is shown, the corresponding timeline frame is shown
- presenter can make one or the other frame reduced

## TODO
- svg: set style for each branch
- add a masking layer in the svg image
- in svg: make clickable
 