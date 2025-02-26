import events from "./Events.js";


const template = document.createElement('template');
template.innerHTML = `
    <style>
    
        :host {
            flex-grow: 0;
            width: 400px;
        }
        
        #tags_container {
            margin: 20px 20px 20px 0px;
            padding: 0px 15px 15px 15px;
            border-radius: 10px;
            border: 2px solid var(--colour-1);
            color: var(--colour-1);
        }
        
        #tag {
            visibility: hidden;
            width: fit-content;
            padding: 10px 15px;
            border-radius: 10px;
            border: 2px solid var(--colour-2);
            color: var(--colour-2);
        }
        
    </style>
    <div id="tags_container">
        <p>Tags</p>
        <div id="tag">Sport</div>
    </div>
</div>
`;


export default class Tags extends HTMLElement {
    constructor() {
        super();

        this.on_tag_changed = this.on_tag_changed.bind(this);
    }

    on_tag_changed(tag) {
        this.tag_element.style.visibility = 'visible';
        this.tag_element.innerText = tag;
    }

    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.tag_element = template_element.getElementById('tag');
            this.shadowRoot.appendChild(template_element);
        }

        events.register_callback('tag_changed', this.on_tag_changed);
    }

    disconnectedCallback() {
        events.unregister_callback('tag_changed', this.on_tag_changed);
    }
}

window.customElements.define("k-tags", Tags);