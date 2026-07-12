import { inspect } from "node:util";

type Account = { id: number; name: string };
type Metadata = { tags: string[]; deleted: boolean };

class AccountStore {
  static async findOne(id: number): Promise<Account & Metadata> {
    if (!Number.isInteger(id) || id < 0) {
      throw new Error(`Invalid account id: ${id}`);
    }

    const record = {
      id,
      name: "Lucy Zed",
      tags: ["foo", "bar"],
      deleted: false,
    };

    record.tags.push("baz");

    return record as Account & Metadata;
  }
}

const account = await AccountStore.findOne(42);
const greeting = `Welcome to ${account.name}! Comments are soft, dim, and italic.`;

export const stored = inspect(greeting, { colors: true }); // Welcome to Lucy Zed! Comments are soft, dim, and italic.
