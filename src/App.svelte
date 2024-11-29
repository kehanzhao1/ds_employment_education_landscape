
<script>
  import Scrolly from "./Scrolly.svelte";
  import { fade } from 'svelte/transition';
  import { onMount } from "svelte";
  import * as d3 from 'd3'; 
  import LineCompare from "./linecompare.svelte";
  import BarchartScrolly from "./barchartScrolly.svelte";
  let value;
  let data= [];
  const steps = [    {
      heading: "How many jobs are there?",
      paragraph: "DS employment has grown rapidly from <50k in 2019 to 190k in 2023, much faster than statisticians and Software developers.",
    },
    {
      heading: "Is the pay competitive?",
      paragraph: "DS annual mean wage stands at 119k, lower than software developer's $138k, but higher than statistician $109K and national average $64k.",
    },
    {
      heading: "Who employs the most DS?",
      paragraph: "IT related companies employ 11% of data scientists, followed by insurance",
    },
    {
      heading: "👨🏻‍💻Which role pays the most?",
      paragraph: "R&D followed by IT pays over 115k annually",
    }
  ];

  let introVisible = false;

  onMount(() => {
    const mainHeading = d3.select(".mainheading h1");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          // Trigger when .mainheading is no longer fully visible
          if (entry.boundingClientRect.top < 0) {
            introVisible = true;
          }
        });
      },
      {
        root: null, // Use the viewport
        threshold: 0, // Trigger as soon as the element enters/leaves the viewport
        rootMargin: "-100px 0px 0px 0px", // Start observing 100px before it scrolls out of view
      }
    );

    observer.observe(mainHeading.node());
  });

</script>




<main>
   <div class="mainheading">
     <h1>DATA SCIENCE EMPLOYMENT AND EDUCATION</h1>
     <p>There is a growing demand for data scientists due to explosion of data; many education institutions have also began offering Data Science titled degrees and curriculum.</p>
   </div>
  <section class="intro" class:intro-visible={introVisible}>
    <h1> 👨🏻‍💻Hottest job of the 21st century? </h1>
    <p>
    In this exploration, we scraped LinkedIn and community college data to uncover the employment, education landscape. Is the education offering meeting the industry's needs? And are community colleges equipped to offer the necessary training?
    </p>
  </section>
  <div class="subheading">
  <h1> What does the Employment Landscape Look Like?</h1>
   </div>
<div class="container">
  <div class="scrolly">
    <Scrolly bind:value>
      {#each steps as step, i}
      <div class="step" class:active={value === i} on:click={() => value = i}>
        <h2 >{step.heading}</h2>
        <p>{step.paragraph}</p>
      </div>
      {/each}
    </Scrolly>
  </div>
  
  <div class="graph" style="position: relative; height: 400px;"> <!-- Adjust height as needed -->
    <div style="position: absolute; top: 0; left: 0; right: 7%; display: {value === 0 || value === 1 ? 'block' : 'none'};">
      <LineCompare {value} />
    </div>
    <div style="position: absolute;  top: 0; left: 0; right: 7%; display: {value === 2 || value === 3 ? 'block' : 'none'};">
      <BarchartScrolly {value} />
    </div>
  </div>
</div>


<section class="additional-container">
  <div class="text-content">
    <h2>📈Will the trend continue?</h2>
  </div>
  <div class="text-container">
    <div class="overlay">Growing jobs and graduates</div>
    <ul>
      <li>Employment of data scientists is projected to grow 36 percent from 2023 to 2033, much faster than the average </li>
      <li> ~ 20,800 new openings for data scientists are projected each year</li>
      <li>However, DS graduates have increased to over 46k per year </li>
    </ul>
  </div>
</section>


<div class = 'subheading'>
  <h1>What are the key skills for data scientists</h1> 
  <h2>From the requirements of 100 LinkedIn data science job postings, we compiled the essential education, hard and soft skill requirements asked by industries</h2> 
</div>

<div class = 'subheading'>
  <h1>What do data scientists work on</h1> 
</div>
</main>

<style>
   @font-face {
    font-family: 'Fact';
    src: url('/src/fonts/Fact-ExtraBold.woff2') format('woff2'),
         url('/src/fonts/Fact-ExtraBold.woff') format('woff'),
         url('/src/fonts/Fact-ExtraBold.ttf') format('truetype');
    font-weight: 800; /* Extra bold weight */
    font-style: normal;
  }


   body {
    background-color: #f8f7f5; /* Change this to your desired color */
    margin: 0; /* Remove default margin */
    padding: 0; /* Remove default padding */
    width: 100vw;
    font-family: 'Lato', sans-serif; /* Set a default font family */
  }
  main {
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin:0 auto;
  padding: 0;
}
  .intro {
    margin-bottom: 10vh; /* Add space between the intro section and the container */
    margin-top: 0rem;
    width: 90vw; /* Make the intro section span most of the page */
    margin: 0 auto; /* Center the intro section */
    text-align: center; /* Center the text */
    position: relative; 
    height: auto; /* Adjust height as needed */
    display: flex; /* Center content */
    align-items: center;
    padding:2rem;
    opacity:0;
    transform: translateY(20px); 
    transition: opacity 1s ease-in-out, transform 1s ease-in-out;
  }
  .intro.intro-visible {
    opacity: 1; /* Fully visible */
    transform: translateY(0); /* Back to original position */
  }
  @keyframes slideInFromLeft {
    from {
      opacity: 1;
      transform: translateX(-100%); /* Start off-screen to the left */
    }
    to {
      opacity: 1;
      transform: translateX(0); /* End at the original position */
    }
  }
  .intro h1 {
    margin-bottom: 2rem; /* Add space between the h1 and p elements */
    font-size: 2.5rem; /* Adjust font size as needed */
    font-family: 'Lato', sans-serif;
    font-align: right;
    flex: 1;
    margin-right: 1rem;
    margin-left: 1vw;
    animation: slideInFromLeft 1s ease-in-out;
  }
  .intro p {
    font-size: 1.5rem;
    width: 15vw;
    height: auto;
     /*border: 3.5px solid #141a3e; Add a border around the p element */
    padding: 2.5rem; /* Add padding inside the p element */
   /* Optional: Add rounded corners to the border */
    background-color:       #ffffff;
    border-left: 5px solid #ed5701; /* Add a top border */
    flex: 1 ;
    
    font-family: 'Lato', sans-serif;
    margin-left: 2vw;
    margin-right: 10vw;
  }
 

  .graph {
    flex: 1.2;                                           
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column; 
    margin-left: -6vw;
    margin-right: 5%;
    padding-right: 5rem;
    margin-top: 10vh;
    
  }
  .scrolly {
    flex: 1.5;
    height: 70vh;
    width: auto;
    overflow-y: auto;
    margin-right: 8vw;
    margin-left: 8vw;
    padding-right: 1rem;
    
  }
  .step {
    height: 40vh;
    cursor: pointer; 
    background: #e8e2e2;
    margin-top: 1em;
    text-align: center;
    transition: background 100ms;
    font-family: 'Lato', sans-serif; 
    align-items: center;
    justify-content: center;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
  }
  .step h2 {
    font-size: 2rem; /* Adjust font size as needed */
    margin-bottom: 0.5em; /* Add margin below heading */
    font-family: 'Lato', sans-serif; /* Apply Lato font */
  }
  .step p {
    font-size: 1.5rem; /* Adjust font size as needed */
    padding: 1em; /* Add padding for better readability */
    font-family: 'Lato', sans-serif; /* Apply Lato font */
  }
  
  .step.active {
    background: #cf5029b7;
  }
  
  .step.active h2,.step.active p {
    color: white; /* Change text color to white when active */
    font-weight: bold;;
  }
  section {
    width: 100%;
    margin: 0 auto;
    margin-bottom: 0.5em; 
  }
  
  .spacer {
    height: 10vh;
  }

  
  * {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* Ensure consistent box model */
  
}
 html, body {
  margin: 0; /* Remove default browser margin */
  padding: 0; /* Remove default browser padding */
  width: 100%; /* Ensure body spans full width */
  height: 100%; /* Ensure body spans full height */
 
  overflow-x: hidden; 
}

.banner {
  /* Make sure banner is pinned to the top */
  top: 0;
  left: 0;
  display: flex; /* Center content */
  z-index: 1; /* Ensure banner stays on top of other content */
  background-color: rgb(242, 238, 239);
  background-size: cover; 
  /*background: linear-gradient(to bottom, #031436 15%, rgba(24, 29, 24, 0) 100%);*/   
  color: white;
  padding: 2rem; /* Increase padding for larger banner */
  text-align: center;
  font-size: 2rem; /* Larger font size for the banner title */
  width: 100vw; /* Full viewport width */
  height: 35vh; /* Adjust height for a larger banner (30% of viewport height) */
  box-sizing: border-box; /* Include padding in width/height calculations */
  display: flex; /* Center content */
  justify-content: center; /* Horizontally centered */
  align-items: center; /* Vertically centered */
  margin-top: -5vh;
  margin-left: -50vh;
  margin-right: -50vh;
  margin-bottom: 5vh;
  position: relative;
  border-bottom: 5px solid #73789ea4;
  border-right: 5px solid transparent;
  animation: borderSlideIn 1s ease-in-out;
  border-radius: 10px;
}
@keyframes borderSlideIn {
  from {
    border-bottom-width: 0;
    border-right-width: 0; /* Start with no right border */
  }
  to {
    border-bottom-width: 5px;
    border-right-width: 5px; /* End with the right border */
  }
}

.mainheading h1 {
     /* Take up the left side of the banner */
    display: flex;
    justify-content: center; /* Horizontally centered */
    align-items: center; /* Vertically centered */
    color: #ed5701; /* Set font color to black */
    position: relative;
    font-size: 4.5rem; 
    font-family:  'Fact', sans-serif; 
    font-weight: 800; /* Set font weight to bold */
    margin-top: 20vh;
    margin-bottom: 5vh;
  }
  .mainheading p {
     /* Take up the left side of the banner */
    display: flex;
    justify-content: center; /* Horizontally centered */
    align-items: center; /* Vertically centered */
    color: #6b6060d2; /* Set font color to black */
    position: relative;
    font-size: 26px; 
    font-family:  'Lato', sans-serif; 
    margin-top: 0vh;
    margin-bottom: 10vh;
  }
  .subheading h1 {
     /* Take up the left side of the banner */
    display: flex;
    justify-content: center; /* Horizontally centered */
    align-items: center; /* Vertically centered */
    color: #271103; /* Set font color to black */
    position: relative;
    font-size: 3rem; 
    font-family:  'Fact', sans-serif; 
    font-weight: 800; /* Set font weight to bold */ 
    margin-top: 10vh;
    margin-bottom: 5vh;
  }
  .subheading h2 {
     /* Take up the left side of the banner */
    display: flex;
    justify-content: center; /* Horizontally centered */
    align-items: center; /* Vertically centered */
    color: #6b6060d2; /* Set font color to black */
    position: relative;
    font-size: 26px; 
    font-family:  'Lato', sans-serif; 
    margin-top: 0vh;
    margin-bottom: 10vh;
  }
  .banner .text img {
    position: relative;
    order: 2;
    /* Align the image to the right */
    /* Center the image vertically */
    transform: translateX(-5%);
    transform: translateY(5%); /* Adjust for vertical centering */
    height: 160px; /* Adjust the height as needed */
    width:10vw; /* Maintain aspect ratio */
    margin-left: -1rem; /* Space between text and image */
  }
    /* Optional: Style the scrollbar */
    .scrolly::-webkit-scrollbar {
    width: 11px;
  }

  .scrolly::-webkit-scrollbar-thumb {
    background-color: #d3d6e2;
    border-radius: 4px;
  }

  .scrolly::-webkit-scrollbar-thumb:hover {
    background-color: #d3d6e2;
  }

  .additional-container {
    display: flex;
    margin-top: 5vh;
    padding: 2rem;
    align-items: center;
    width: 100vw;
    margin-bottom: 10vh;
  }

  .text-container {
    position: relative;
    flex: 1.3;
    padding: 1rem;
    background-color: rgb(245, 238, 235);
    border-left: 5px solid #ed5701;
    border-radius: 12px;
    font-family: 'Lato', sans-serif;
    margin-left: 0vw;
    margin-right: 25%;
    height:40vh;
    min-width: 300px;
    width: 50vw auto;
    overflow: auto; /* Allow scrolling if content exceeds height */
    word-wrap: break-word; /* Wrap long words */
    overflow-wrap: break-word; /* Ensure wrapping for text */
    
  }

  .text-container ul {
    list-style-type: disc;
    padding-left: 1rem;
    
  }
  .text-container li {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }
  .text-content h2 {
    font-family: 'Lato', sans-serif;
    font-size: 2.5rem;
    margin-bottom: 1rem;
    margin-right: 5vw;
    margin-left: 5vw;
    flex:0.7
  }
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(68, 49, 43, 0.8); /* Semi-transparent background */
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    border-radius: 12px;
    cursor: pointer;
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  .text-container:hover .overlay {
    opacity: 0;
    transform: scale(1.05);
  }
  .container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 100vw;
    height: 100vh;
    margin-top: 10vh;
  }

</style>
