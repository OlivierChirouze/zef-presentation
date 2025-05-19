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


# Get ready for presenting

- for this presentation:
  - [ ] 🖥️ shell: start serving the presentation `npm run start`
  - [ ] 🌐 Browser: (of course) open the presentation (http://localhost:8100)
  - [ ] Mobile: open the presentation as well, directly from github for simplicity (https://olivierchirouze.github.io/zef-presentation/)
- for Petole project
  - [ ] 🧑‍💻 WebStorm: debug backend (`npm run backend:run`)
  - [ ] 🖥️ shell: start frontend `npm run frontend:start`
  - [ ] 🔌 connect phone with cable
    - [ ] 📱 install **local** Petole app on phone
    - [ ] 📱 open app
    - [ ] 📱 login
  - [ ] 🌐 Chrome: debug devices
  - [ ] 🌐 Browser: open http://localhost:8102/
    - [ ] 🌐 login
  - [ ] 🗃️ start Mongo client (ex: NoSQLBooster for MongoDB)
- for "A Place to Live" project
  - [ ] 🧑‍💻 WebStorm: debug backend
  - [ ] 🖥️ shell: start frontend