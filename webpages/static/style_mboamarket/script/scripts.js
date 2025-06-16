//  script toogle barre de navigation sur mobile
//  script toogle barre de navigation sur mobile 
//  script toogle barre de navigation sur mobile




// Script Du Loading De Ma Page Account.html
// Script Du Loading De Ma Page Account.html
// Script Du Loading De Ma Page Account.html

 document.getElementById('menu-toggle').addEventListener('click', function() {
    const menu = document.getElementById('navmenu');
    menu.classList.toggle('hidden');
  });
//  script toogle barre de navigation sur mobile
//  script toogle barre de navigation sur mobile

 // Attendre que le DOM soit complètement chargé
  document.addEventListener('DOMContentLoaded', function() {
    // Récupérer les éléments avec vérification
    const loader = document.getElementById('loader');
    const mainContent = document.getElementById('mainContent');
    
    // Vérifier que les éléments existent
    if (!loader || !mainContent) {
      console.error('Éléments introuvables ! Vérifiez les IDs dans votre HTML');
      return;
    }

    // Fonction pour cacher le loader
    function hideLoader() {
      loader.style.opacity = '0';
      setTimeout(() => {
        loader.style.display = 'none';
        mainContent.style.opacity = '1';
      }, 500);
    }

    // Cacher le loader quand la page est chargée
    function handleLoad() {
      // Minimum 1.5s d'affichage pour éviter le flash
      setTimeout(hideLoader, 1500);
    }

    // Démarrer le processus
    if (document.readyState === 'complete') {
      handleLoad();
    } else {
      window.addEventListener('load', handleLoad);
      // Timeout de sécurité après 5s
      setTimeout(handleLoad, 5000);
    }
  });

// Script Du Loading De Ma Page Account.html
// Script Du Loading De Ma Page Account.html


 // Simule le chargement de la page (à remplacer par votre vraie logique)
  window.addEventListener('load', function() {
    // Cache le loader après un délai
    setTimeout(function() {
      document.getElementById('loader').classList.add('opacity-0');
      document.getElementById('content').classList.remove('opacity-0');
      
      // Retire complètement le loader du DOM après l'animation
      setTimeout(function() {
        document.getElementById('loader').style.display = 'none';
      }, 500); // Doit correspondre à la durée de la transition (500ms)
    }, 2000); // Durée minimale d'affichage du loader (2 secondes)
  });

  // Solution alternative si la page est déjà chargée
  document.addEventListener('DOMContentLoaded', function() {
    if (document.readyState === 'complete') {
      document.getElementById('loader').style.display = 'none';
      document.getElementById('content').classList.remove('opacity-0');
    }
  });




  document.addEventListener('DOMContentLoaded', function() {
  const container = document.querySelector('.carousel-container');
  const slides = document.querySelectorAll('.carousel-slide');
  const prevBtn = document.querySelector('.carousel-prev');
  const nextBtn = document.querySelector('.carousel-next');
  const indicators = document.querySelectorAll('.carousel-indicator');
  const actualiteLinks = document.querySelectorAll('.actualite-link');
  
  let currentIndex = 0;
  let intervalId;
  const slideInterval = 5000;
  
  function updateLinks() {
    const currentSlide = slides[currentIndex];
    const actualiteId = currentSlide.getAttribute('data-actualite-id');
    const institutionId = currentSlide.getAttribute('data-institution-id');
    
    actualiteLinks.forEach(link => {
      link.href = `/view_actualitys/${actualiteId}/${institutionId}/`;
    });
  }
  
  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.style.opacity = i === index ? '1' : '0';
    });
    
    indicators.forEach((indicator, i) => {
      indicator.classList.toggle('bg-white', i === index);
      indicator.classList.toggle('w-4', i === index);
      indicator.classList.toggle('w-2', i !== index);
    });
    
    currentIndex = index;
    updateLinks();
  }
  
  function nextSlide() {
    const newIndex = (currentIndex + 1) % slides.length;
    showSlide(newIndex);
  }
  
  function startAutoRotation() {
    intervalId = setInterval(nextSlide, slideInterval);
  }
  
  prevBtn.addEventListener('click', () => {
    clearInterval(intervalId);
    const newIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(newIndex);
    startAutoRotation();
  });
  
  nextBtn.addEventListener('click', () => {
    clearInterval(intervalId);
    nextSlide();
    startAutoRotation();
  });
  
  indicators.forEach((indicator, i) => {
    indicator.addEventListener('click', () => {
      clearInterval(intervalId);
      showSlide(i);
      startAutoRotation();
    });
  });
  
  showSlide(0);
  startAutoRotation();
  
  container.addEventListener('mouseenter', () => clearInterval(intervalId));
  container.addEventListener('mouseleave', startAutoRotation);
});