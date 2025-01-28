export async function saveToIndexedDB(key, data) {
  const db = await openDB("recollection", 1, {
    upgrade(db) {
      db.createObjectStore("screenshots");
    },
  });
  await db.put("screenshots", data, key);
}

export async function getFromIndexedDB(key) {
  const db = await openDB("recollection", 1);
  return await db.get("screenshots", key);
}
