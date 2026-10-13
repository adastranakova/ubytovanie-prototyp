<?php

$internat = null;
$chyba = null;
$pripojene = false;

try {
    $config = require __DIR__ . '/config.php';

    $dsn = sprintf(
        'mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
        $config['host'],
        $config['port'],
        $config['database']
    );

    $pdo = new PDO(
        $dsn,
        $config['username'],
        $config['password'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );

    $pripojene = true;

    $vysledok = $pdo->query(
        'SELECT id, nazov FROM internat WHERE id = 1'
    );

    $internat = $vysledok->fetch();
} catch (Throwable $e) {
    $chyba = 'Nepodarilo sa načítať údaje z databázy.';
    error_log($e->getMessage());
}
?>
<!DOCTYPE html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Žiadosť o ubytovanie B – prototyp</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 0 20px;
            line-height: 1.6;
        }

        .uspech {
            color: #176b32;
        }

        .chyba {
            color: #b42318;
        }
    </style>
</head>
<body>
    <h1>Žiadosť o ubytovanie B</h1>
    <p>Triviálny prototyp prepojenia PHP a MySQL.</p>

    <?php if ($chyba !== null): ?>
        <p class="chyba">
            <?= htmlspecialchars($chyba, ENT_QUOTES, 'UTF-8') ?>
        </p>
    <?php elseif ($pripojene): ?>
        <p class="uspech">Pripojenie k databáze funguje.</p>

        <?php if ($internat): ?>
            <p>
                Dostupný internát:
                <strong>
                    <?= htmlspecialchars(
                        $internat['nazov'],
                        ENT_QUOTES,
                        'UTF-8'
                    ) ?>
                </strong>
            </p>
        <?php else: ?>
            <p>Vzorový internát s ID 1 sa v databáze nenachádza.</p>
        <?php endif; ?>
    <?php endif; ?>
</body>
</html>
