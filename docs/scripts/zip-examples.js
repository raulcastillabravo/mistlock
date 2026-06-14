import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { ZipArchive } from 'archiver';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SRC_DIR = path.resolve(__dirname, '../../src');
const OUTPUT_DIR = path.resolve(__dirname, '../public/downloads');

const IGNORE_PATTERNS = [
  '**/node_modules/**',
  '**/.venv/**',
  '**/venv/**',
  '**/__pycache__/**',
  '**/.aws-sam/**',
  '**/.pytest_cache/**',
  '**/.terraform/**',
  '**/.firebase/**',
  '**/tmp/**',
  '**/*.pyc',
  '**/.DS_Store'
];

/**
 * Recursively compresses a folder into a ZIP archive applying exclusions
 * @param {string} sourceDir 
 * @param {string} outputFilePath 
 * @returns {Promise<number>} Final size in bytes
 */
async function zipFolder(sourceDir, outputFilePath) {
  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(outputFilePath);
    const archive = new ZipArchive({ zlib: { level: 9 } });

    output.on('close', () => {
      resolve(archive.pointer());
    });

    archive.on('error', (err) => {
      reject(err);
    });

    archive.pipe(output);

    archive.glob('**/*', {
      cwd: sourceDir,
      dot: true, // Include hidden files like .env, .vscode, and .devcontainer
      ignore: IGNORE_PATTERNS
    });

    archive.finalize();
  });
}

async function main() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  if (!fs.existsSync(SRC_DIR)) {
    throw new Error(`Source directory not found: ${SRC_DIR}`);
  }

  const providers = fs.readdirSync(SRC_DIR).filter(item => {
    return fs.statSync(path.join(SRC_DIR, item)).isDirectory() && !item.startsWith('.');
  });

  const examplesToZip = providers.flatMap(provider => {
    const providerPath = path.join(SRC_DIR, provider);
    return ['mves', 'projects'].flatMap(type => {
      const typePath = path.join(providerPath, type);
      if (!fs.existsSync(typePath)) return [];

      return fs.readdirSync(typePath)
        .filter(item => fs.statSync(path.join(typePath, item)).isDirectory())
        .map(example => ({
          examplePath: path.join(typePath, example),
          zipPath: path.join(OUTPUT_DIR, `${provider}-${type}-${example}.zip`)
        }));
    });
  });

  const sizes = await Promise.all(
    examplesToZip.map(({ examplePath, zipPath }) => zipFolder(examplePath, zipPath))
  );
  const totalBytes = sizes.reduce((acc, bytes) => acc + bytes, 0);

  const totalMb = (totalBytes / (1024 * 1024)).toFixed(2);
  console.log(`\nCompression finished! Generated ${examplesToZip.length} ZIP files. Total size: ${totalMb} MB`);
}

await main();
