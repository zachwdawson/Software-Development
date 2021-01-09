## Self-Evaluation Form for Milestone 1

### General 

We will run self-evaluations for each milestone this semester.  The
graders will evaluate them for accuracy and completeness.

Every self-evaluation will go out into your Enterprise GitHub repo
within a short time afrer the milestone deadline, and you will have 24
hours to answer the questions and push back a completed form.

This one is a practice run to make sure you get


### Specifics 


- does your analysis cover the following ideas:

  - the need for an explicit Interface specification between the (remote) AI 
    players and the game system?
    
    - Yes, in the line "The next software component is the “plug-in” protocol for the player, 
        which we will refer to as a software interface for the AI players of Fish. 
        This interface will interact with the representation of the pieces of the game to 
        provide endpoints to the player around the actions needed to complete a Fish game." 
        (2nd paragraph, 1st line in system.pdf)



  - the need for a referee sub-system for managing individual games
  
    - Yes, in the line "We would also have a component of a runner of games or more simply a “referee”. This component 
    would make sure that the AI players are following the AI player interface (not cheating and malfunctioning) 
    as well as be able to move the game along (removing tiles in the beginning, assigning penguin color, 
    running placement rounds, moving to next turn, etc.)." (3rd paragraph, 1st line in system.pdf)
    - We could have been more clear about it running a single game, but it is implied by the context.



  - the need for a tournament management sub-system for grouping
    players into games and dispatching to referee components
    
    - Yes, in the line "Outside of a single game of Fish, we would need to develop a component to manage tournaments of Fish. 
    This component would allow players to sign-up for the tournament (which includes specifying a time period for sign-ups),
     create matchups (which will include AI players that have implemented the player interface) 
     and announcing winners and losers of the tournament" (4th paragraph, 1st line in system.pdf)
    - Also in the line "match players and referees" (4th paragraph, 3rd to last line)



- does your building plan identify concrete milestones with demo prototypes:

  - for running individual games
  
    - Yes, under the heading "Milestone 1: Demo a single game of Fish being played locally" in milestones.pdf
    - We specify local as a single computer


  - for running complete tournaments on a single computer 
  
    - Yes, under the heading "Milestone 2: Demo a single tournament of Fish being run locally:" in milestones.pdf
    - We specify local as a single computer


  - for running remote tournaments on a network
    
    - Yes, under the heading "Milestone 3: Demo a remote tournament of Fish:" in milestones.pdf





- for the English of your memo, you may wish to check the following:

  - is each paragraph dedicated to a single topic? does it come with a
    thesis statement that specifies the topic?
    
    - Yes, each paragraph is about a single component or milestone. 
    - They mostly start with a sentence specifying the component or milestone.
    - The last paragraph in system.pdf could have specified that it is a component for viewing instead of
      "Finally, the players (or other stakeholders) would want to see how their player is doing."



  - do sentences make a point? do they run on?
  
    - We feel that the sentences make a point and do not run on and are stripped down to saying the most they 
    can about the components.
    - There were a few spots parentheses were overused to explain ideas such as "(removing tiles in the beginning, 
    assigning penguin color, running placement rounds, moving to next turn, etc.)." in the 3rd paragraph of system.pdf




  - do sentences connect via old words/new words so that readers keep
    reading?
    
    - We believe that the sentences connect in their internal structure and across paragraphs.
    - For example, we bring in together a lot of our ideas in talking about the tournament manager component: 
    "Outside of a single game of Fish, we would need to develop a component to manage 
    tournaments of Fish. This component would allow players to sign-up for the tournament (which includes specifying
     a time period for sign-ups), create matchups (which will include AI players that have implemented the player 
     interface) and announcing winners and losers of the tournament." (4th paragraph of system.pdf)
     


  - are all sentences complete? Are they missing verbs? Objects? Other
    essential words?
    
    - we could not find any incomplete sentences in our evaluations of our memos



  - did you make sure that the spelling is correct? ("It's" is *not* a
    possesive; it's short for "it is". "There" is different from
    "their", a word that is too popular for your generation.)
    
    - The last sentence of the 1st paragraph of milestones.pdf is missing a period
    - In the last sentence of the 1st paragraph of milestone 1 (in milestones.pdf) we are missing a right parentheses around "who will be terminated"
    - In the last sentence of the 2nd paragraph of system.pdf we use the word "implanted" by accident instead of implemented.



The ideal feedback are pointers to specific senetences in your memo.
For PDF, the paragraph/sentence number suffices. 

For **code repos**, we will expect GitHub line-specific links. 


