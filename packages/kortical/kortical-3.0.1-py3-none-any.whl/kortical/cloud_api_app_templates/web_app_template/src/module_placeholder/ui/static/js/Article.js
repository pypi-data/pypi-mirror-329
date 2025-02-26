import events from "./Events.js";


const template = document.createElement('template');
template.innerHTML = `
    <style>
    
        :host {
            flex-grow: 1;
            width: auto;
            padding: 20px;
        }
        
        #article_container {
            display: flex;
            flex-direction: column;
            height: 100%;
            padding: 0px 15px 15px 15px;
            border-radius: 10px;
            border: 2px solid var(--colour-1);
            color: var(--colour-1);
            box-sizing: border-box;
        }
        
        #article {
            flex-grow: 1;
            width: 100%;
            height: auto;
            box-sizing: border-box;
        }
        
    </style>
    <div id="article_container">
        <p>Article</p>
        <textarea id="article" placeholder="Paste article content here..."></textarea>
    </div>
</div>
`;


export default class Article extends HTMLElement {
    constructor() {
        super();

        this.on_article_change = this.on_article_change.bind(this);
    }

    on_article_change(e) {
        // Call model
        fetch('predict',
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({input_text: e.currentTarget.value})
            })
            .then(function (value) {
                return value.text()
            })
            .then(function (value) {
                events.on_event('tag_changed', value);
            })
            .catch(function (reason) {
                alert(reason)
            });
    }

    connectedCallback() {
        if (!this.shadowRoot) {
            this.attachShadow({mode: 'open'});
            const template_element = template.content.cloneNode(true);
            this.shadowRoot.appendChild(template_element);
        }

        this.article_element = this.shadowRoot.getElementById('article');
        this.article_element.addEventListener('input', this.on_article_change, false);
    }

    disconnectedCallback() {
        this.article_element.removeEventListener('input', this.on_article_change);
    }
}

window.customElements.define("k-article", Article);