
const template = document.createElement('template');
template.innerHTML = `
    <style>
        :host {
            display: block;
            padding-bottom: 15px;
            position: relative;
        }
        :host::after {
            content: '';
            position: absolute;
            left: 0;
            top: 100%;
            display: block;
            width: 100%;
            height: 25px;
            background: linear-gradient(#1A1823, #00000000);
            z-index: 1;
        }
        * {
            box-sizing: border-box;
        }
        .header-inner {
            display: flex;
            align-items: center;
            padding: 5px;
        }
        .title {
            font-size: 16px;
            font-weight: 700;
            line-height: 19px;
            margin: 0 0 4px 0;
            letter-spacing: .5px;
        }
        .status-wrap {
            margin-left: 20px;
        }
        .status-icon {
            font-size: 12px;
            line-height: 12px;
            margin: 0;
        }
        .status-icon::before {
            content: '';
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        .online {
            color: var(--success);
        }
        .online::before {
            background-color: var(--success);
        }
        .offline {
            color: var(--danger);
        }
        .offline::before {
            background-color: var(--danger);
        }
    </style>
    <div class="header-inner">
        <img src="./static/images/k-logo-blue.svg">
        <div class="status-wrap">
            <p class="title">Kortical Chat</p>
            <p id="status" class="status-icon">Online</p>
        </div>
    </div>
`;


export default class Header extends HTMLElement {
    constructor() {
        super();
        this.status_element = null;
        this.on_status_change = this.on_status_change.bind(this);
    }

    on_status_change(status) {
        if(status) {
            this.status_element.classList.add("online");
            this.status_element.classList.remove("offline");
        } else {
            this.status_element.classList.remove("online");
            this.status_element.classList.add("offline");
        }
    }


    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.status_element = template_element.getElementById('status');
            this.shadowRoot.appendChild(template_element);
        }

        if(navigator.onLine) {
            this.on_status_change(true);
        } else {
            this.on_status_change(false);
        }

        window.addEventListener("offline", (e) => {
            this.on_status_change(false);
        });
        window.addEventListener("online", (e) => {
            this.on_status_change(true);
        });
    }
}

window.customElements.define("k-header", Header);