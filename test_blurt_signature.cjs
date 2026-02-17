const blurt = require('@blurtfoundation/blurtjs');

// Configurar Blurt
blurt.config.set('address_prefix', 'BLT');
blurt.config.set('chain_id', 'cd8d90f29ae273abec3eaa7731e25934c63eb654d55080caff2ebb7f5df6381f');

async function testBlurtSignature() {
    try {
        console.log('=== Testing Blurt Signature ===\n');

        // Clave de prueba (reemplaza con una clave real para probar)
        const testKey = '5JYourPrivateKeyHere'; // CAMBIAR POR UNA CLAVE REAL

        // Crear una transacción de prueba
        const tx = {
            ref_block_num: 12345,
            ref_block_prefix: 67890,
            expiration: new Date(Date.now() + 60000).toISOString().slice(0, -5),
            operations: [
                ['vote', {
                    voter: 'testuser',
                    author: 'testauthor',
                    permlink: 'test-post',
                    weight: 10000
                }]
            ],
            extensions: []
        };

        console.log('Transaction to sign:', JSON.stringify(tx, null, 2));
        console.log('\nChain ID:', blurt.config.get('chain_id'));
        console.log('Address Prefix:', blurt.config.get('address_prefix'));

        // Intentar firmar
        console.log('\n=== Attempting to sign ===');
        const signedTx = blurt.auth.signTransaction(tx, [testKey]);

        console.log('\nSigned transaction:', JSON.stringify(signedTx, null, 2));
        console.log('\n✅ Signature successful!');

    } catch (error) {
        console.error('\n❌ Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

// Mostrar métodos disponibles
console.log('Available blurt.auth methods:', Object.keys(blurt.auth));
console.log('Available blurt.config methods:', Object.keys(blurt.config));
console.log('\n');

testBlurtSignature();
