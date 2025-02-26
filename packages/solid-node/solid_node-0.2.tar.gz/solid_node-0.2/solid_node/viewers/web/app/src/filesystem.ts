export interface FileNode {
  name: string;
  path: string;
  isFile: boolean;
  children?: FileNode[];
}

export const loadTree = async (path: string): Promise<FileNode> => {
  const tstamp = new Date().getTime(); // avoid cache
  const response = await fetch(`/file${path}?t=${tstamp}`);
  if (!response.ok) {
    throw new Error('Failed to load file tree');
  }
  return response.json() as Promise<FileNode>;
};
