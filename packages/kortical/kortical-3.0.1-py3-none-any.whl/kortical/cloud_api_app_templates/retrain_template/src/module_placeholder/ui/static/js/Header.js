

const template = document.createElement('template');
template.innerHTML = `
    <style>
        header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--bg-form);
            margin-bottom: 50px;
        }
        
        .navbar-brand {
            display: flex;
            align-items: center;
        }
    </style>
    <header>
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid">
                <span class="navbar-brand d-flex">
                    <img src="static/images/k-logo.svg" alt="Korticall Logo" class="me-2" />
                    <div id="navbar__title"></div>
                </span>
            </div>
        </nav>
    </header>
`;

class Header extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.appendChild(template.content.cloneNode(true));
        this.title_element = this.querySelector('#navbar__title');

        this.title_element.innerText = window.app_title;
    }
}

window.customElements.define("k-header", Header);