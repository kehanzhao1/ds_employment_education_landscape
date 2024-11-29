<script>
  import { createEventDispatcher } from 'svelte';
  import { onMount } from 'svelte';
  export let value = undefined;
  const dispatch = createEventDispatcher();

  let steps;
  let observer;

  onMount(() => {
    steps = document.querySelectorAll('.step');
    console.log('Steps:', steps); // Debug steps

    observer = new IntersectionObserver(handleIntersect, {
      root: null,
      rootMargin: '0px',
      threshold: 0.5
    });

    steps.forEach(step => {
      console.log('Observing step:', step); // Debug each step being observed
      observer.observe(step);
    });
  });

  function handleIntersect(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const index = Array.from(steps).indexOf(entry.target);
        value = index;
        //console.log('Intersecting step index:', index); // Debug intersecting step index
        console.log('Value', value); // Debug intersecting step index
        dispatch('input', { value });
      }
    });
  }
</script>

<div>
    <slot></slot>
</div>

<style>
  .step {
    opacity: 0.5;
    transition: opacity 0.5s;
  }

  .step.active {
    opacity: 1;
  }
  .scrolly {
    flex: 1;
  }
  .graph {
    flex: 1;
  }
  
</style>