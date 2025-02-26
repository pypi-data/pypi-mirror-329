

const template = document.createElement('template');
template.innerHTML = `
    <style>
    
        :host {
            display: flex;
            flex-direction: row;
            align-items: center;
            height: 80px;
            width: 100%;
            color: var(--background-colour);
            font-weight: bold;
            font-size: 30px;
            background-image: linear-gradient(90deg, var(--colour-1), var(--colour-2));
        }
        
        #logo {
            height: 60px;
            padding-left: 20px;
            padding-right: 20px;
        }
        
        .title {
        
        }
        
    </style>
    <img id="logo"><div id="app_title" class="title"></div>&nbsp;<div id="app_title_extension" class="title"></div>
</div>
`;


export default class Header extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            const logo_element = template_element.getElementById('logo');
            logo_element.src = window.logo_image_url;
            const app_title_element = template_element.getElementById('app_title');
            app_title_element.innerText = window.app_title;
            const app_title_extension_element = template_element.getElementById('app_title_extension');
            app_title_extension_element.innerText = window.app_title_extension;
            this.shadowRoot.appendChild(template_element);
        }
    }
}

window.customElements.define("k-header", Header);