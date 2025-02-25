document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("webauthn-setup").addEventListener("click", async () => {
        // https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredentialCreationOptions
        const options = {
            challenge: Uint8Array.from(document.getElementById('webauthn-challenge').textContent, c => c.charCodeAt(0)),
            rp: {
                name: "music player",
            },
            user: {
                id: Uint8Array.from(document.getElementById("webauthn-identifier").textContent, c => c.charCodeAt(0)),
                name: document.getElementById("webauthn-username").textContent,
                displayName: document.getElementById("webauthn-displayname").textContent,
            },
            authenticatorSelection: {
                residentKey: "required",
            },
            pubKeyCredParams: [{alg: -7, type: "public-key"}],
            attestation: "none",
        };
        console.debug("options", options);
        const credential = await navigator.credentials.create({publicKey: options});
        console.debug('credential', credential);
        /** @type {AuthenticatorAttestationResponse} */
        const response = credential.response;

        // clientDataJSON contains type==webauthn.create, origin, random challenge
        // https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorResponse/clientDataJSON
        const clientDataJsonB64 = btoa(String.fromCharCode(...new Uint8Array(response.clientDataJSON)));

        // new method to easily get public key in DER format
        // saves much hassle of decoding CBOR data, manually extracting bits from binary data, and then convert the key to DER format.
        // https://www.w3.org/TR/webauthn-2/#sctn-public-key-easy
        // https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorAttestationResponse/getPublicKey
        const publicKey = btoa(String.fromCharCode(...new Uint8Array(response.getPublicKey())));

        await jsonPost("/account/webauthn_setup", {client: clientDataJsonB64, public_key: publicKey});
        alert("Set up successfully");
    });
})
