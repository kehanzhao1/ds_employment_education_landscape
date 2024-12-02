
<script>
  import Scrolly from "./Scrolly.svelte";
  import { fly } from 'svelte/transition';
  import { onMount } from "svelte";
  import * as d3 from 'd3'; 
  import LineCompare from "./linecompare.svelte";
  import BarchartScrolly from "./barchartScrolly.svelte";
  import EmploymentMap from "./employmentMap.svelte";
  import Skillbarchart from "./skillbarchart.svelte";
  import DADSMap from './DADSMap.svelte';
  import DSDegMap from './DSDegMap.svelte';
  import DSClassMap from './DSClassMap.svelte';
  import VoronoiMap from './VoronoiMap.svelte';
  import SkillsBarChart from "./SkillsBarChart.svelte";

  let value;
  const steps = [    {
      heading: "🙇‍♂️How many jobs are there?",
      paragraph: "DS employment has grown rapidly from <50k in 2019 to 190k in 2023, much faster than statisticians and Software developers",
    },
    {
      heading: "💰Is the pay competitive?",
      paragraph: "DS annual mean wage stands at 119k, lower than software developer's $138k, but higher than statistician $109K and national average $64k",
    },
    {
      heading: "🤝Who employs the most DS?",
      paragraph: "IT related companies employ 11% of data scientists, followed by insurance",
    },
    {
      heading: "👨🏻‍💻Which role pays the most?",
      paragraph: "R&D followed by IT pays over 115k annually",
    }
  ];
  
  let openBox = null;
  // Titles and contents for the boxes
  let boxes = [
  { id: 1, title: '1. Building Machine Learning Models', content: 'Design and deploy cutting edge machine learning models to develop innovative solutions to business challenges.' },
  { id: 2, title: '2. Analysis and Insights Discovery', content: 'Use statistical techniques to analyze complex datasets to uncover trends, drive product growth, streamline workflows and optimize processes.' },
  { id: 3, title: '3. Collaboration Across Teams', content: 'Work closely with cross-functional teams, including product and engineering, to align data science initiatives with overall objectives.' },
  { id: 4, title: '4. Reporting and Delivering Impact', content: 'Create dashboards, visualizations and report insights to technical and non-technical stakeholders to drive impactful results in the business.' }
   ];

// Function to toggle the box
const toggleBox = (id) => {
    boxes = boxes.map((box) =>
      box.id === id ? { ...box, revealed: !box.revealed } : box
    );
  };
 
  let introVisible = false;

  onMount(() => {
    const mainHeading = d3.select(".mainheading h1");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.boundingClientRect.top < 0) {
            introVisible = true;
          }
        });
      },
      {
        root: null, 
        threshold: 0, 
        rootMargin: "-100px 0px 0px 0px", 
      }
    );

    observer.observe(mainHeading.node());
  });

  const CCPath = '/cc_with_coor.csv';
  let selectedVar = 'DS';

  let sections = [0, 0.2, 0.4, 0.6, 0.8]; 
  let currentSection = 0; 

  function handleScroll() {
    const scrollPosition = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    currentSection = sections.findIndex((threshold, index) => 
      scrollPosition >= threshold && (index === sections.length - 1 || scrollPosition < sections[index + 1])
    );
  }
  function scrollToSection(index) {
    const targetScroll = sections[index] * (document.body.scrollHeight - window.innerHeight);
    window.scrollTo({ top: targetScroll, behavior: 'smooth' });
  }
</script>



<svelte:window on:scroll={handleScroll} />
<main>
  <div class="progress-bar">
    {#each sections as _, index}
      <div class="dot {index === currentSection ? 'active' : ''}"
      on:click={() => scrollToSection(index)}
      ></div>
    {/each}
  </div>

   <div class="mainheading">
     <h1>DATA SCIENCE EMPLOYMENT AND EDUCATION</h1>
     <p>There is a growing demand for data scientists due to explosion of data; many education institutions have also began offering Data Science titled degrees and curriculums...</p>
   </div>
  <section class="intro" class:intro-visible={introVisible}>
    <h1> 👨🏻‍💻Hottest job of the 21st century? </h1>
    <p>
    In this exploration, we scraped LinkedIn and community college data to uncover DS employment, education landscape. Is the education offering meeting industry needs? Are community colleges equipped to offer the necessary training?
    </p>
  </section>
  <div class="subheading">
  <h1> What does the Employment Landscape Look Like?</h1>
  <h2>Let's first explore the key summary statistics of Data Science jobs in the U.S. from Bureau of Labor Statistics.</h2>
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
  <div class="graph" style="position: relative; height: 400px;"> 
    <div style="position: absolute; top: 0; left: 0; right: 7%; display: {value === 0 || value === 1 ? 'block' : 'none'};">
      <LineCompare {value} />
    </div>
    <div style="position: absolute;  top: 0; left: 0; right: 7%; display: {value === 2 || value === 3 ? 'block' : 'none'};">
      <BarchartScrolly {value} />
    </div>
  </div>
</div>
<div class="subheading">
  <h2>States like California and Texas are leading the employment of data scientists.</h2>
   </div>
<div>
  <EmploymentMap />
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
      <li>However, DS graduates have also increased to over 46k per year </li>
      <li>Whether the market will be saturated will depend on many factors</li>
    </ul>
  </div>
</section>


<div class = 'subheading'>
  <h1>What skills are needed to become a data scientist?</h1> 
  <h2>From the requirements of 100 LinkedIn data science job postings, we compiled the essential education, hard and soft skill requirements asked by industries</h2> 
</div>
<section class="intro" class:intro-visible={introVisible}>
  <h1> 🎓 Are degrees needed? </h1>
  <p>
    <br>
    <span style="font-weight: bold; font-size: 2.2rem; font-family : 'Fact', sans-serif; color : steelblue">60%</span> of postings mentioned degree, 
    <span style="font-weight: bold; font-size: 2.2rem; font-family : 'Fact', sans-serif; color : steelblue;">49%</span> mentioned Master's and 
    <span style="font-weight: bold; font-size: 2.2rem; font-family : 'Fact', sans-serif; color : steelblue;">30%</span> mentioned PhD
  </p>
</section>


<div> <Skillbarchart ></Skillbarchart></div>
<div class = 'subheading'>
  <h2>Comparing to a 2018 study, the current job market emphasize more on&nbsp;
    <span style= "color :steelblue;"> Machine Learning, AI & LLMs</span> </h2>
</div>


<div class = 'subheading'>
  <h1>What do data scientists work on?</h1> 
  <h2>Despite being an interdisciplinary field, the key responsibilites of DS from 100 job posts can be summarised to 4 main tasks.</h2>
</div>

<div class="boxwrapper">
  <div class="boximage">
    <img src="/robot.png" alt="robot Image" />
  </div>
<div class="workcontainer">
  {#each boxes as { id, title, content, revealed }}
    <div class="box {revealed ? 'revealed' : 'hidden'}" on:click={() => toggleBox(id)}>
      <div class="box-content">
        {#if revealed}
        <p class="content" >{content}</p>
        {:else}
          <span class = "box-title">{title}</span>
        {/if}
      </div>
    </div>
  {/each}
</div>
</div>

<div class = 'subheading'>
  <h2>Key takeaway: to become a data scientist in 2024, one needs to have both cutting edge
    <span style="color: steelblue;">technical skills in ML and communication ability.</span>
  </h2>
</div>


  <div class='subheading'>
    <h1>In the U.S., what does data science education at the community college level look like?</h1>
    <h2>Data science education programs at four-year universities and at the graduate level have grown tremendously in recent years. Is this growth reflected at two-year institutions?</h2>

    <p>
      Community colleges are postsecondary schools that offer certificates and two-year programs that are aimed at preparing students for the workforce.
      Students attend community colleges for a variety of reasons—some enter with the goal of transferring to a four-year institution, others aim to gain the necessary skills to immediately enter the workforce.
      something something
      <br>
      <br>
      In our research, we investigated every community college in the U.S. to see if they offered any certificates or degrees relating to data science and data analytics.
      <br>
      <br>
      Below is an interactive map that shows the frequencies of: colleges that offer a data science certificate or degree, colleges that offer data analytics or data science certificiate or degree, or colleges that offer a data science introductory course.
      Use the drop down menu to switch between variables.   
    </p>
  </div>

  <div class='mapcontainer'>
    <label for="var-select">Select Variable to Visualize: </label>
    <select id="job-select" bind:value={selectedVar}>
      <option value="DS">Data Science Degree or Certificate Offered</option>
      <option value="DSDA">Data Science or Data Analytics Degree or Certificate Offered</option>
      <option value="DSCourse">Data Science Course Offered</option>
    </select>
  
    <div>
      {#if selectedVar === "DS"}
        <DSDegMap CCPath={CCPath} variableToVisualize="numDS" />
      {:else if selectedVar === "DSDA"}
        <DADSMap CCPath={CCPath} />
      {:else if selectedVar === "DSCourse"}
        <DSClassMap CCPath={CCPath} />
      {/if}
    </div>
  </div>

  <div class='subheading'>
    <h1>What community colleges near data science job hubs offer data science degrees?</h1>
  </div>

  <div class='textpara'>
    <p>
      In the following map, we use data from this <a href="https://huggingface.co/datasets/lukebarousse/data_jobs">source</a> to identify the cities in the U.S. with the post job postings for data related jobs.
      This data includes information on job postings made in the year 2023, for jobs related to data, such as data science, data analysis, and data engineering. 
      There were a little over 200,000 data jobs located in the United States in this dataset.
    </p>
  </div>
  
  <div class='textpara' >
    <p>
      We then created a Voronoi diagram to analyze which data hub each community college is closest to. 
      Hover over each region to see which community colleges offer a data science degree.
      Please zoom in to explore!
    </p>
  </div>

  <div class='mapcontainer'>
    <VoronoiMap />
  </div>

  <div class='subheading'>
    <h1>How do coding languages and frameworks at community colleges differ from jobs?</h1>

    <p>
      In the bar chart below, we visualize the frequencies of coding languages and frameworks we found in our research on community college data analytics and science programs.
      The frequencies of these skills were then calculated for the data jobs dataset.
      Selecting the "Job Positions" button will animate the bar chart to show how the frequencies of these skills change from their prevelance in community college curriculumns, to actual job postings.
    </p>
  </div>

  <SkillsBarChart />

  <div class="acknowledgment">
   <span style= "color :darkgrey;">Presented by  <span>  Kehan Zhao, Sarah Song, Atticus Ginsborg  <span style= "color :darkgrey;"> </span>
   <br>
   <br>
   December 2024
  </div>
 
</main>


<style>
   @font-face {
    font-family: 'Fact';
    src: url('/src/fonts/Fact-ExtraBold.woff2') format('woff2'),
         url('/src/fonts/Fact-ExtraBold.woff') format('woff'),
         url('/src/fonts/Fact-ExtraBold.ttf') format('truetype');
    font-weight: 800; 
    font-style: normal;
  }

  * {
  margin: 0;
  padding: 0;
  box-sizing: border-box; 
  
}

*, *::before, *::after {
    box-sizing: inherit;
}
  
  main {
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height:100%;
  margin:0 auto;
  margin-right: 0vw;
  padding: 0;
  overflow-x: visible;
}
  .intro {
    margin-bottom: 30vh; 
    margin-top: 1rem;
    margin-right: 0vw;
    width: 90vw; 
    margin: 0 auto; 
    text-align: center; 
    position: relative; 
    height: 100%; 
    display: flex; 
    align-items: center;
    justify-content: center;
    padding: 2rem;
    opacity:0;
    transform: translateY(20px); 
    transition: opacity 1s ease-in-out, transform 1s ease-in-out;
  }
  .intro.intro-visible {
    opacity: 1; 
    transform: translateY(0); 
  }
  @keyframes slideInFromLeft {
    from {
      opacity: 1;
      transform: translateX(-100%);
    }
    to {
      opacity: 1;
      transform: translateX(0); 
    }
  }
  .intro h1 {
    font-size: 2.5rem; 
    font-family: 'Lato', sans-serif;
    font-align: right;
    flex: 1;
    margin-right: 2rem;
    margin-left: 0vw;
    animation: slideInFromLeft 1s ease-in-out;
  }
  .intro p {
    font-size: 1.5rem;
    width: 30vw;
    height: 30vh;
    padding: 2.5rem; 
    background-color:       #ffffff;
    border-left: 5px solid #cf5029b7;
    flex: 1 ;
    font-family: 'Lato', sans-serif;
    margin-left: 0vw;
    margin-right: 15vw;
    box-sizing: border-box;
    align-items: center;
    justify-content: center;
  }
 

  .graph {
    flex: 1.2;                                           
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column; 
    margin-left: -6vw;
    margin-right: 5vw;
    padding-right: 3rem;
    margin-top: 10vh;
    
  }
  .container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 100vw;
    height: 100vh;
    margin-top: 10vh;
    margin-bottom: -5vw;
    padding: 1vh 2vw;
    box-sizing: border-box;
  }

  .mapcontainer {
      display: flex;
      flex-direction: column; 
      align-items: center; 
      gap: 20px;
      padding: 20px;
  }

  .textpara {
    display: flex;
    justify-content: center; 
    align-items: center;
    color: #000000d2; 
    position: relative;
    font-size: 20px; 
    font-family:  'Lato', sans-serif; 
    margin-top: 2vh;
    margin-bottom: 0vh;
    text-align: left;
  }

  .scrolly {
    flex: 1.5;
    height: 70vh;
    width: auto;
    overflow-y: auto;
    margin-right: 5vw;
    margin-left: 8vw;
    padding-right: 1rem;
    box-sizing: border-box;
    
  }
  .step {
    height: 40vh;
    width: auto;
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
    font-size: 2rem; 
    margin-bottom: 0.5em; 
    font-family: 'Lato', sans-serif; 
  }
  .step p {
    font-size: 1.5rem;
    padding: 1em;
    font-family: 'Lato', sans-serif; 
  }
  
  .step.active {
    background: #cf5029b7;
  }
  
  .step.active h2,.step.active p {
    color: white; 
    font-weight: bold;;
  }
  section {
    width: 100%;
    margin: 0 auto;
    margin-bottom: 0.5em; 
  }
  
.mainheading h1 {
    display: flex;
    justify-content: center; 
    align-items: center; 
    color: #ed5701;
    position: relative;
    font-size: 4.5rem; 
    font-family:  'Fact', sans-serif; 
    font-weight: 800; 
    margin-top: 30vh;
    margin-bottom: 5vh;
  }
  .mainheading p {
    display: flex;
    justify-content: center; 
    align-items: center; 
    color: #6b6060d2; 
    position: relative;
    font-size: 26px; 
    font-family:  'Lato', sans-serif; 
    margin-top: 0vh;
    margin-bottom: 10vh;
  }
  .subheading h1 {
    display: flex;
    justify-content: center;
    align-items: center; 
    color: #271103; 
    position: relative;
    font-size: 3rem; 
    font-family:  'Fact', sans-serif; 
    font-weight: 800; 
    margin-top: 20vh;
    margin-bottom: 5vh;
  }
  .subheading h2 {
    justify-content: center; 
    align-items: center; 
    color: #6b6060d2; 
    position: relative;
    font-size: 26px; 
    font-family:  'Lato', sans-serif; 
    margin-top: 0vh;
    margin-bottom: 0vh;
  }

  .subheading p {
    display: flex;
    justify-content: center; 
    align-items: center;
    color: #000000d2; 
    position: relative;
    font-size: 20px; 
    font-family:  'Lato', sans-serif; 
    margin-top: 2vh;
    margin-bottom: 0vh;
    text-align: left;
  }
  .subheading span {
    display: inline; 
  }
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
    margin-top: -5vh;
    padding: 2rem;
    align-items: center;
    width: 100vw;
    margin-bottom: 10vh;
  }

  .text-container {
    position: relative;
    flex: 1;
    padding: 1rem;
    background-color: rgb(245, 238, 235);
    border-left: 5px solid #cf5029b7;
    border-radius: 12px;
    font-family: 'Lato', sans-serif;
    margin-left: 0vw;
    margin-right: 30vw;
    height:35vh;
    min-width: 300px;
    width: 40vw auto;
    overflow-y: auto; 
    overflow-x: hidden;
    word-wrap: break-word; 
    overflow-wrap: break-word; 
    box-sizing: border-box; 
    
  }

  .text-container ul {
    list-style-type: disc;
    padding-left: 2rem;
    padding-right: 2rem
    
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
    margin-left: 2vw;
    flex:0.7
  }
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(128, 92, 82, 0.8); 
    height:100%;
    width: 100%;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.7rem;
    font-family: 'Lato', sans-serif;
    border-radius: 12px;
    cursor: pointer;
    transition: opacity 0.3s ease, transform 0.3s ease;
    pointer-events: auto;
  }
  .text-container:hover .overlay {
    opacity: 0;
    transform: scale(1.05);
  }
  .workcontainer {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 3rem;
    width: 100%;
    max-width: 600px;
    margin: auto;
    margin-top: 10vh;
    margin-bottom: 10vh;
  }

  .box {
    padding: 1rem;
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 1rem;
    cursor: pointer;
    height: 180px; 
    width: 350px; 
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    border: none;
    padding: 1rem;
  }

  .box-content {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    font-family: 'Lato', sans-serif;
    font-size: 18px;
  }

  .box-title{
    font-size: 1.5rem;
    font-weight: bold;
    font-family: 'Fact', sans-serif;
    color: #ffffff;
  }

  .box.hidden {
    background-color: #cf5029b7;
  }

  .box.revealed {
    background-color: #e8e2e2; 

  }
  .boxwrapper {
    display: flex;
    align-items: flex-start;
    gap: 2rem;
    max-width: 900px;
    margin: auto;
    padding: 1rem;
  }

  .boximage {
    max-width: 250px;
    flex-shrink: 0;
    margin-top: 20vh;
    margin-left: -15vw;
    margin-right: 3vw;
  }

  .boximage img {
    width: 100%;
    height: auto;
   
  }
  .progress-bar {
    position: fixed;
    top: 50%;
    left: 40px;
    transform: translateY(-40%);
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background-color: lightgray;
    transition: background-color 0.2s;
  }

  .dot.active {
    background-color:#ed5701;
  }
   
  
  .acknowledgment {
    width: 100%;
    padding: 15px;
    background-color: #ffffff;
    color: #271103;
    text-align: center;
    position: relative;
    bottom: 0;
    left: 0;
    margin-top: 25vh;
    margin-bottom: 5vh;
  }

  .acknowledgment span {
    font-size: 1rem;
    font-family: "Fact", sans-serif;
    font-weight: 800;
    
  }
</style>
